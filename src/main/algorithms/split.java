//https://leetcode.com/problems/split-strings-by-separator/
class Solution {
    public List<String> splitWordsBySeparator(List<String> words, char separator) {
        ArrayList<String> new_words = new ArrayList();
        for (String s : words){
            String[] s_array = s.split("\\"+separator);
            for(String ss : s_array){
                if(!ss.isEmpty()){
                    new_words.add(ss);
                }
            }
        }
        return new_words;
    }    
}

//https://leetcode.com/problems/split-a-string-in-balanced-strings/
class Solution {
    public int balancedStringSplit(String s) {
        char[] c = s.toCharArray();
        int count_L=0;
        int count_R=0;
        int sum=0;
        for(int i=0;i<c.length;i++){
            if(c[i]=='L'){
                count_L ++;
            }else{
                count_R ++;
            }
            if(count_L==count_R){
                sum ++;
                count_R =0;
                count_L =0;
            }
        }
        return sum;
    }
}

//https://leetcode.com/problems/split-with-minimum-sum/
class Solution {
    public int splitNum(int num) {
        char[] c = String.valueOf(num).toCharArray();
        Arrays.sort(c);
        StringBuilder sb1 = new StringBuilder();
        StringBuilder sb2 = new StringBuilder();
        for (int i =0; i<c.length;i++){
            if(i%2==0){
                sb1.append(c[i]);
            }else{
                sb2.append(c[i]);
            }
        }
        int num1 = !sb1.isEmpty() ? Integer.parseInt(sb1.toString()) :0;
        int num2 = !sb2.isEmpty() ? Integer.parseInt(sb2.toString()) :0;
        return num1+num2;
    }
}