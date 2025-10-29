//LLM creativity level
const TEMPERATURE = 1;

//Hua Bai: API configuration
//OpenAI API
var openAIPath = "https://api.openai.com/v1/chat/completions";
var openAIImageModelPath = "https://api.openai.com/v1/images/generations";
var openAIKey = "sk-svcacct-on6Afy0ikigp-Y2XUjRtLzIHW-g0biSNPOnbjV8c-zva8XV5FA";
var OPEN_AI_MODEL = "gpt-4o-mini-2024-07-18";
var OPEN_AI_IMAGE_MODEL = "dall-e-3";
var OPEN_AI_IMAGE_RESOLUTION = "1024x1024";

//Gemini API
//This api key is free with limited requests
var geminiKey = "AIzaSyAX1Ola5vutWExrk-T740JiJbnybUBKfBw";
var geminiPath = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=" + geminiKey;
var GEMINI_MODEL = "gemini-1.5-flash";

//Hua Bai: exchangable variables
var currentPremise;
var currentOpenAIRecipe;
var currentGeminiRecipe;

// Draw the home page --- author:Kexin Ma
document.write ( `
    <div class="apiKeyPicture">
        <div class="titlePicture">
    		<div class="titleDiv">Good and Smart Recipes</div>
    		<label class="titleLable">Special note: AI-generated recipes are not always correct and may contain recommendations that go against common cooking and medical knowledge. We strongly recommend that people with cooking experience use this system.</label>
    	</div>
		<div class="apiKeyDiv" id="apikeyDiv">
			<input class="apiKeyInput" id="apikey" type="text" placeholder="Enter your OpenAI API KEY"/>
			<button class="buttonEnter" id="enterDetail">Enter</button>
			<p style="margin-left:15px" id="error_apiKey"></p>
		</div>
		<div id="recipe-block">
	    </div>
	</div>
` );

// Draw a recipe page --- author:Kexin Ma
const openRecipeTemplate = `
<div class="container" id="detail">
	<div class="box_input" id="getData" style="float: left;">
		<div id="getRecipe">
		    <div>
				<label>Select your gender <span class="required">*</span></label>
				<select id="gender">
					<option value="male" aria-checked="true">Male</option>
					<option value="female">Female</option>
				</select>
			</div>
			<div>
				<label>Enter your age <span class="required">*</span></label>
				<textarea onblur="checkFormat(2)" rows="1" id="age" placeholder="e.g. 18"></textarea>
				<p id="errorMsg_age"></p>
			</div>
			<div>
				<label>Select your physical condition <span class="required">*</span></label>
				<select id="physicalStatus">
					<option value="Healthy" aria-checked="true">Healthy</option>
					<option value="Fatigued">Fatigued</option>
					<option value="Stressed">Stressed</option>
					<option value="Nauseous">Nauseous</option>
					<option value="Dehydrated">Dehydrated</option>
					<option value="Pain">Pain</option>
					<option value="Dizzy">Dizzy</option>
					<option value="Weak">Weak</option>
					<option value="Sore">Sore</option>
					<option value="Congested">Congested</option>
					<option value="Recovering">Recovering</option>
					<option value="Swollen">Swollen</option>
					<option value="Underweight">Underweight</option>
					<option value="Overweight">Overweight</option>
					<option value="Alert">Alert</option>
				</select>
			</div>
			<div>
				<label>Enter the foods you have in your refrigerator </label>
				<textarea onblur="checkFormat(1)" rows="2" id="existFood" placeholder="e.g. potatoes, carrots"></textarea>
				<p id="errorMsg_existFood"></p>
			</div>
			<div>
				<label for="avoidFood">Enter foods you avoid </label>
				<textarea onblur="checkFormat(0)" id="avoidFood" placeholder="e.g. celery, pepper" rows="2"></textarea>
				<p id="errorMsg_avoidFood"></p>
			</div>
			<button id="submitRecipe" onclick="getRecipe()">Submit</button>
		</div>
	</div>
	<div id="loading" class="loading hidden" style="float: right;">
          <div class="loadingText"></div>
          <p>loading ...</p>
    </div>
	<iframe class="box_answer" style="display: none;" id="source1">
	</iframe>
	<iframe class="box_answer" style="display: none;" id="source2">
	</iframe>
	<div class="modal-overlay" id="modal">
      <div class="modal-content">
        <button class="close-btn" id="closeModal">&times;</button>
        <div>
          <h2 id="compareTitle"></h2>    
          <div class="box_answer" id="compareResults" style="width:94%;white-space:pre;overflow-x:auto;max-width:100%;overflow-y:auto;max-heighth:100%"></div>
        </div>
      </div>
    </div>
</div>
`;

// API inputs --- author:Kexin Ma
const enterDetail = document.getElementById("enterDetail");
const apikey = document.getElementById("apikey");

// Hua Bai: http headers building
const getOpenAIHeader = () => {
    var key = `Bearer ${openAIKey}`;
    if (apikey != null && apikey.length > 0) {
        key = `Bearer ${apikey}`;
    }
    return {
        "Authorization": key,
        "Content-Type": "application/json"
    };
};
const getGeminiHeader = () => {
    return {
        "Content-Type": "application/json"
    };
};

//Hua Bai: OpenAI generation
async function callOpenAI(prompt, generationMod) {
    if (generationMod === "text") {
        const headers = getOpenAIHeader();
        const requestBody = {
        	"model": OPEN_AI_MODEL,
            "messages": [{
    			"role": "user",
    			"content": prompt
    		}],
            "temperature": TEMPERATURE
        };
        console.log("OpenAI text request: ", requestBody);
        const response = await fetch(openAIPath, {
            method: "POST",
            mode: "cors",
            cache: "no-cache",
            headers: headers,
            body: JSON.stringify(requestBody)
        });
        json_res = await response.json();
        console.log("OpenAI text Reponse:", json_res);
        choice0 = json_res.choices[0];
        choice0msg = choice0.message;
        if (choice0msg.role != "assistant") {
            console.log("not correct role: ", choice0msg);
        }
        return choice0msg.content;
        
    } 
    if (generationMod === "image") {
        const headers = getOpenAIHeader();
        const requestBody = {
            	"model": OPEN_AI_IMAGE_MODEL,
    	        "prompt": prompt,
    	        "n": 1,
    	        "size": OPEN_AI_IMAGE_RESOLUTION
        };
        console.log("OpenAI image request: ", requestBody);
        const response = await fetch(openAIImageModelPath, {
            method: "POST",
            mode: "cors",
            cache: "no-cache",
            headers: headers,
            body: JSON.stringify(requestBody)
        });
        json_res = await response.json();
        console.log("OpenAI image reponse:", json_res);
        return json_res.data[0].url;
    }
    
    console.log("OpenAI invalid prompt type: ", generationMod);
}

//Kexin Ma: Gemini generation
async function callGemini(prompt, generationMod) {
    if (generationMod === "text") {
        const headers = getGeminiHeader();
        const requestBody = {
            "contents": [{
    			"parts": [{
    			    "text": prompt
    			}]
    		}]
        };
        console.log("Gemini text request: ", requestBody);
        const response = await fetch(geminiPath, {
            method: "POST",
            mode: "cors",
            headers: headers,
            body: JSON.stringify(requestBody)
        });
        json_res = await response.json();
        console.log("Gemini text Reponse:", json_res);
        resMsg = json_res.candidates[0].content.parts[0].text;
        return resMsg;
    }
    
    console.log("Gemini invalid prompt type: ", generationMod);
}

function buildRecipeGenerationPrompt(age, gender, bodyCondition, foodInStock, foodAvoid) {
    var patternLine = "I'm a " + age +"-year-old " + gender +", my body condition: "+ bodyCondition + ". ";
    if (foodInStock != null && foodInStock.length > 0) {
        patternLine += "I have these foods in refrigerator: " + foodInStock + ". ";
    }
    if (foodAvoid != null && foodAvoid.length > 0) {
        patternLine += "I cannot eat these foods: "+ foodAvoid +". "
    }
    currentPremise = patternLine;
    patternLine += "Could you recommend only one recipe for my daily breakfast? "
        + "Please just return the recipe, not quotation of my question, not any greeting ending. Because I want to use the response to show in another place and I don't want to revise it.";
    return patternLine;
}

function buildRecipeImagePrompt(recipe) {
    return "Here is a recipe:\n" + recipe + "\nPlease generate one image about it."
}

function buildCompareRecipePrompt() {
    var prompt = currentPremise + "\n\n" +
        "recipe 1: \n" +
        currentOpenAIRecipe + "\n\n" +
        "recipe 2: \n" +
        currentGeminiRecipe + "\n\n" +
        "If I need to choose only one from the two recipes, which one is more suitable?"
    return prompt;
}

async function compareRecipeTo(anotherRecipe) {
    var comparePrompt = buildCompareRecipePrompt();
    console.log("comparePrompt", comparePrompt);
    // if (true) {
    //     return comparePrompt;
    // }
    //recipe1 stands for OpenAI, if another recipe is from OpenAI,
    //then current recipe is from Gemini, we need to ask Gemini.
    //Likewise.
    if (anotherRecipe === "recipe1") {
        return await callGemini(comparePrompt, "text");
    } else {
        return await callOpenAI(comparePrompt, "text");
    }
}

//Hua Bai: hit both OpenAI and Gemini to generete two recipes and two images
async function doGetRecipes(age, gender, bodyCondition, foodInStock, foodAvoid) {
    console.log("getRecipe request params: ", age, gender, bodyCondition, foodInStock, foodAvoid);
    // openAIRecipeImage = "https://www.inspiredtaste.net/wp-content/uploads/2019/10/Homemade-Apple-Pie-Recipe-6-1200.jpg";
    // geminiRecipeImage = "https://www.inspiredtaste.net/wp-content/uploads/2019/10/Homemade-Apple-Pie-Recipe-6-1200.jpg";
    var recipeGenerationPrompt = buildRecipeGenerationPrompt(age, gender, bodyCondition, foodInStock, foodAvoid);
    //Call the two AI APIs respectively
    var openAIRecipe = await callOpenAI(recipeGenerationPrompt, "text");
    // var openAIRecipe = "Vegetable Omelette with Whole Grain Toast\n\nIngredients:\n- 3 large eggs\n- 1/4 cup milk (or dairy-free alternative)\n- 1/2 bell pepper, diced\n- 1/4 cup onion, diced\n- 1/2 cup spinach, chopped\n- Salt and pepper to taste\n- Olive oil or cooking spray\n- 2 slices of whole grain bread\n- Optional toppings: avocado, salsa, or cheese\n\nInstructions:\n1. In a bowl, whisk together the eggs, milk, salt, and pepper until well combined.\n2. Heat a non-stick skillet over medium heat and add a little olive oil or cooking spray.\n3. Sauté the onion and bell pepper for about 3-4 minutes, until softened.\n4. Add the spinach and cook for an additional minute until wilted.\n5. Pour the egg mixture into the skillet, tilting the pan to ensure an even distribution of vegetables.\n6. Cook for about 4-5 minutes, or until the edges start to set. Gently lift the edges with a spatula to allow uncooked eggs to flow to the edges.\n7. Once the top is just slightly runny, fold the omelette in half and let it cook for another minute.\n8. While the omelette is cooking, toast the whole grain bread.\n9. Serve the omelette on a plate with the toast on the side. Add optional toppings as desired. Enjoy!";
    var geminiRecipe = await callGemini(recipeGenerationPrompt, "text");
    // var geminiRecipe = "**Savory Oatmeal with Spinach and Feta**\n\n* 1/2 cup rolled oats\n* 1 cup water or milk (dairy or non-dairy)\n* 1 cup spinach, chopped\n* 1/4 cup crumbled feta cheese\n* 1 tablespoon olive oil\n* Salt and pepper to taste\n\n\nInstructions:\n\n1. Heat olive oil in a small saucepan over medium heat. Add spinach and cook until wilted, about 2 minutes.\n2. Add oats and water/milk to the saucepan. Bring to a boil, then reduce heat and simmer for 5-7 minutes, or until oats are cooked through and liquid is absorbed.\n3. Stir in feta cheese, salt, and pepper. Serve warm.\n";
    //Get an image for the each recipe
    var openAIRecipeImagePrompt = buildRecipeImagePrompt(openAIRecipe);
    var geminiRecipeImagePrompt = buildRecipeImagePrompt(geminiRecipe);
    //Gemini does not support HTTP requests to generate images for the moment,
    //since the keys are the different recipes, we use OpenAI to generate
    //the both recipe's image
    var openAIRecipeImage = await callOpenAI(openAIRecipeImagePrompt, "image");
    var geminiRecipeImage = await callOpenAI(geminiRecipeImagePrompt, "image");
    //set overall exchangable variables
    currentOpenAIRecipe = openAIRecipe;
    currentGeminiRecipe = geminiRecipe;
    //build response
    return {
        openAI: {
            recipe: openAIRecipe,
            recipeImage: openAIRecipeImage
        },
        gemini: {
            recipe: geminiRecipe,
            recipeImage: geminiRecipeImage           
        }
    }
}

// Open a recipe page --- author:Kexin Ma
const openRecipe = () => {
    console.log("Opening Recipe");
    document.getElementById("recipe-block").innerHTML = openRecipeTemplate;
    // Render page
    //drawPage();
};

// Verify input parameters --- author:Kexin Ma
// checkFlag: All verify passed flag
var checkFlag = false;
const checkFormat= (flag) => {
    console.log("start checkFormat");
    //error message be used to innerHTML
	var errorMsg="";
	var inputObject="";
	// flag==1 is existFood, 0 is avoidFood, 2 is age
	if(flag==1){
		errorMsg = document.getElementById('errorMsg_existFood');
		inputObject = document.getElementById('existFood').value.trim();
	}else if(flag==0){
		errorMsg = document.getElementById('errorMsg_avoidFood');
		inputObject = document.getElementById('avoidFood').value.trim();
	}else{
		errorMsg = document.getElementById('errorMsg_age');
		inputObject = document.getElementById('age').value.trim();
	}
	
	if(inputObject != ''){
	    var pattern = "";
	    var errorMsg_content=""
	    if(flag==2){
	        //age: All numbers with spaces before and after
	        pattern = /^\s*\d+\s*$/;
	        errorMsg_content = 'Incorrect! Must numbers ! e.g. 18';
	    }else{
	        //existFood,avoidFood: One or more letters number space, space + comma + one or more letters: one or more
	        pattern = /^[a-zA-Z0-9 ]+(\s*,\s*[a-zA-Z0-9 ]+)*$/;
	        errorMsg_content = 'Incorrect! Can letters,numbers,space, and separated by commas! e.g. potatoes, carrots';
	    }
        //meet the requires
		if (pattern.test(inputObject)) {
			errorMsg.textContent = ''; 
			checkFlag=true;
		} else {
			errorMsg.textContent = errorMsg_content;
			checkFlag=false;
		}
	}else{
	    if(flag==2){// age cannot empty
	        errorMsg.textContent = 'Incorrect! Cannot be empty! e.g. 18'; 
	        checkFlag=false;
	    }else{
	        errorMsg.textContent = ''; 
	        checkFlag=true;
	    }
	}
	console.log("end checkFormat")
};

// compare with another recipe --- author:Kexin Ma
//flag=1 is compare with 2, flag=2 is compare with 1
const compareTo= async (flag) => {
        console.log("start compareTo----------"+flag)
        const closeModalBtn = document.getElementById("closeModal");
        //open compare modal
        const modal = document.getElementById("modal");
        modal.classList.add("show");
        var compareResults = document.getElementById("compareResults");
        var compareTitle = document.getElementById("compareTitle");
        if (compareResults.textContent !== "") {
            compareResults.textContent = ""; 
        }
        showLoading();
        //get compare results
        var result = await compareRecipeTo(flag);
        hideLoading();
        compareTitle.textContent = "Compare details with "+ flag;
        if(result!=""&&result!=null){
            compareResults.textContent = result; 
        }else{
            compareResults.textContent = "No results returned!"; 
        }

    //   document.getElementById("compareResults").textContent = result;
    //   document.getElementById("compareTitle").textContent = "Compare details with "+ flag;
     
      //close compare modal
      closeModalBtn.addEventListener("click", () => {
        modal.classList.remove("show");
      });
      
      //close compare modal
      modal.addEventListener("click", (e) => {
        if (e.target === modal) {
          modal.classList.remove("show");
        }
      });
      console.log("end compare")
};

const showLoading= () => {
  const loading = document.getElementById("loading");
  loading.classList.remove("hidden");
}
		
const hideLoading= () => {
  const loading = document.getElementById("loading");
  loading.classList.add("hidden");
}


// Display results --- author:Kexin Ma
const getRecipe = async () => {
    console.log("start get recipe");
    
    // All inputs are verified. If verification fails, submission is not allowed.
    if (!checkFlag) {
        // Avoid clicking Submit without performing any action
        checkFormat(2);
		return;
	}
    
    // Get input value
    var gender = document.getElementById("gender").value;
	var age = document.getElementById("age").value;
	var existFood = document.getElementById("existFood").value;
	var avoidFood = document.getElementById("avoidFood").value;
	var physicalStatus = document.getElementById("physicalStatus").value;
	console.log("age--"+age+"gender--"+ gender+"physicalStatus--"+ physicalStatus+"existFood--"+ existFood+"avoidFood--"+ avoidFood);
	showLoading(); 
    var recipes = await doGetRecipes(age, gender, physicalStatus, existFood,avoidFood);
    console.log("got recipes", recipes);
    hideLoading();
    if( recipes!=null && recipes!= ""){
        const getDataDiv = document.getElementById("getData");
    	if (getDataDiv) {
    	  getDataDiv.remove(); 
    	}
    }else{
        console.log("fail to get recipes")
        return;
    }
	// Show results
	const source1 = document.getElementById("source1");
	source1.style.display = "block";
	const source2 = document.getElementById("source2");
	source2.style.display = "block";
	
    setTimeout(() => { // Set a waiting time to avoid A without loading
        // add iframe to use scrollbars 
	    const iframeSource1 = source1.contentDocument || source1.contentWindow.document;
	    const iframeSource2 = source2.contentDocument || source2.contentWindow.document;
	    // verify that the iframe has been obtained
	    if (iframeSource1 && iframeSource1.body) {
	        //draw the recipe1 iframe
            const label = document.createElement('label');
            label.textContent = "Recipe 1 from OpenAI";
            var buttonText = null;
            //add compare buttom
            if(recipes.openAI.recipe!=null && recipes.openAI.recipe!=""){
                buttonText = iframeSource1.createElement('button');
                buttonText.style.marginLeft = "20px"; 
                buttonText.textContent = "Compare with another";
                buttonText.addEventListener('click', function() {
                    compareTo("recipe2");
                });     
            }
            label.style.color = "black"; 
            label.style.fontSize = "18px"; 
            label.style.fontWeight = "bold"; 
            var content = null;
            if(recipes.openAI.recipe!=null && recipes.openAI.recipe!=""){
                content = document.createElement("div");
                content.id = "content1";
                content.style.whiteSpace = "pre";
                content.style.marginBottom="10px"
                content.style.marginTop = "10px";  
                content.style.color = "black";       
                content.textContent = recipes.openAI.recipe;
            }
            var pic = null;
            if(recipes.openAI.recipeImage!=null && recipes.openAI.recipeImage!=""){
                pic = iframeSource1.createElement("div");
                pic.id = "pic1";
                const imgAnswer = iframeSource1.createElement("img");
                imgAnswer.src = recipes.openAI.recipeImage; 
                imgAnswer.style.width = "100%";
                imgAnswer.style.height = "auto";
                imgAnswer.style.objectFit = "cover";
                pic.appendChild(imgAnswer);
            }
            iframeSource1.body.appendChild(label);
            if (buttonText) {
                iframeSource1.body.appendChild(buttonText);
            }
            if (content) {
                iframeSource1.body.appendChild(content);
            }
            if (pic) {
                iframeSource1.body.appendChild(pic);
            }
            
	    }else{
	        console.log("fail load iframeSource1")
	    }
	    if (iframeSource2 && iframeSource2.body) {
	        //draw the recipe2 iframe
            const label = document.createElement('label');
            label.textContent = "Recipe 2 from Google Gemini AI";
            var buttonText2 = null;
            if(recipes.gemini.recipe!=null && recipes.gemini.recipe!=""){
                buttonText2 = iframeSource2.createElement('button');
                buttonText2.style.marginLeft = "20px"; 
                buttonText2.textContent = "Compare with another";
                buttonText2.addEventListener('click', function() {
                    compareTo("recipe1");
                });   
            }
            label.style.color = "black"; 
            label.style.fontSize = "18px"; 
            label.style.fontWeight = "bold"; 
            var content2 = null;
            if(recipes.gemini.recipe!=null && recipes.gemini.recipe!=""){
                content2 = document.createElement("div");
                content2.id = "content2";
                content2.style.whiteSpace = "pre";
                content2.style.marginBottom="10px"
                content2.style.marginTop = "10px";  
                content2.style.color = "black"; 
                content2.textContent = recipes.gemini.recipe;
            }
            var pic2 = null;
            if(recipes.gemini.recipeImage!=null && recipes.gemini.recipeImage!=""){
                pic2 = iframeSource2.createElement("div");
                pic2.id = "pic2";
                const imgAnswer = iframeSource2.createElement("img");
                imgAnswer.src = recipes.gemini.recipeImage; 
                imgAnswer.style.width = "100%";
                imgAnswer.style.height = "auto";
                imgAnswer.style.objectFit = "cover";
                pic2.appendChild(imgAnswer);
            }
            iframeSource2.body.appendChild(label);
            if (buttonText2) {
                iframeSource2.body.appendChild(buttonText2);
            }
            if (content2) {
                iframeSource2.body.appendChild(content2);
            }
            if (pic2) {
                iframeSource2.body.appendChild(pic2);
            }
	    }else{
	        console.log("fail load iframeSource2")
	    }
    }, 200);

};


// Apikey submit Mouse --- author:Kexin Ma
enterDetail.addEventListener("click", () => {
    // If apikey has a value, open the recipe page. 
    if (apikey.value){
        const apikeyDiv = document.getElementById("apikeyDiv");
		if (apikeyDiv) {
		  apikeyDiv.remove(); 
		}
        // console.log("Setting API Key: ", apikey.value);
        apiKey = apikey.value;
        openRecipe();
    }else{
        // If there is no value, please enter it.
        var error_apiKey = document.getElementById("error_apiKey");
        error_apiKey.textContent = 'The input can not empty!';
    }
});

// Apikey submit Keyboard --- author:Kexin Ma
apikey.addEventListener("keyup", function(event) {
    event.preventDefault();
    if (event.keyCode === 13) {
       enterDetail.click();
    }
});



// CSS --- author:Kexin Ma
$('head').append(`<meta charset="utf-8">`);
$('head').append(`<title>Exclusive recipes</title>`);
$('head').append(`<link href='https://fonts.googleapis.com/css?family=Inter' rel='stylesheet'>`);
$('head').append(`<link href='https://fonts.googleapis.com/css?family=Inknut Antiqua' rel='stylesheet'>`);

// Style --- author:Kexin Ma
$('head').append(`
<style>
    .loading {
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: rgba(0, 0, 0, 0.5); /* 半透明背景 */
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      z-index: 9999;
    }


    .loading.hidden {
      display: none;
    }


    .loadingText {
      width: 50px;
      height: 50px;
      border: 6px solid #f3f3f3;
      border-top: 6px solid #3498db;
      border-radius: 50%;
      animation: spin 1s linear infinite;
    }


    .loading p {
      margin-top: 15px;
      color: #fff;
      font-size: 18px;
    }


    @keyframes spin {
      0% {
        transform: rotate(0deg);
      }
      100% {
        transform: rotate(360deg);
      }
    }
    
	.titleDiv{
		font-size: 60px;
		padding-left: 10px;
	}
	.titleLable{
		padding-bottom: 10px;
		font-size: 20px;
		padding-left: 10px;
	}
	.titlePicture{
		// background-image: url('https://ancientbrain.com/uploads/kexinma/recipe.png'); 
		// background-size: contain; 
		margin: 0px 10px 10px 10px;
        border: 1px solid #ccc;
	    border-radius: 8px;
	    padding-top: 10px;
	}
	.apiKeyPicture{
		background-image: url('https://ancientbrain.com/uploads/kexinma/recipe4.jpg'); 
		background-size: contain; 	
		height: 100%;
	}
	.apiKeyInput{
		padding: 5px;
		font-size: 20px;
		margin-left: 15px;
		width: 300px;
	}
    .apiKeyDiv{
		position: inherit;
        margin-left: 30%;
        margin-top: 5%;
	}
	#getRecipe{
	    padding: 15px;
	    display: block; 
	}
	p {
		font-weight: bold;
		display: block;
		margin-top: 0px;
		color: red;
		font-size: 12px;
	}
	label{
		font-weight: bold;
		display: block;
		margin-top: 10px;
	}
    select {
        width: 100%;
        padding: 8px;
        margin-top: 5px;
        border-radius: 5px;
        border: 1px solid #ccc;
    }
	textarea {
	  width: 100%; 
	  box-sizing: border-box; 
	  resize: vertical; 
	  padding: 8px;
	  margin-top: 5px;
	  border-radius: 5px;
	  border: 1px solid #ccc;
	}
	input[type="checkbox"] {
	    margin-top: 10px;
	}
	button {
	    padding: 10px 20px;
	    background-color: #2c74f2;
	    color: white;
	    border: none;
	    border-radius: 5px;
	   // margin-top: 20px;
	    cursor: pointer;
	}
	.buttonEnter{
		  width: 81px;
		  height: 33px;
	}
	button:hover {
	    background-color: #1757c7;
	}
	.container {
        display: flex; 
        justify-content: space-between; 
	}
    .box_input {
        width: 45%; 
        box-sizing: border-box;
		margin: 20px;
		border: 1px solid #ccc;
	    border-radius: 8px;
	    background-color: #f9f8ec;
    }
	.box_answer {
	    padding: 15px;
	    width: 49%; 
	    border: 1px solid #ccc;
	    border-radius: 8px;
	    background-color: #f9f8ec;
	    box-sizing: border-box;
  		height: 70vh;
	  	margin: 20px;
	}
    .required {
        color: red; 
    }
    .modal-overlay {
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: rgba(0, 0, 0, 0.5);
      display: none;
      justify-content: center;
      align-items: center;
      z-index: 1000;
    }

    .modal-content {
      background: white;
      border-radius: 8px;
      padding: 20px;
      width: 80%;
      box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
      text-align: left;
      position: relative;
    }

    .close-btn {
        position: absolute;
        right: 10px;
        color: white;
        border: none;
        border-radius: 30%;
        cursor: pointer;
        font-size: x-large;
        font-weight: bold;
        background-color: red;
    }

    .modal-overlay.show {
      display: flex;
    }
</style>

`);
