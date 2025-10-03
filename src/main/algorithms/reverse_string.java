//https://leetcode.com/problems/reverse-words-in-a-string/
class Solution {
    public String reverseWords(String s) {
        String[] arr = s.trim().split("\\s+");
        StringBuilder sb = new StringBuilder();
        for(int i=arr.length-1;i>=0;i--){
            sb.append(arr[i]);
            if(i>0){
                sb.append(" ");
            }
        }
        return sb.toString();
    }
}

// Difference in one line
//Printable ASCII: Shows an actual symbol (letters, digits, punctuation, space).
//Non-printable ASCII: Special control codes (do not produce a visible symbol, but perform an action).
class Solution {
    public void reverseString(char[] s) {
        int i = 0;
        int k = s.length-1;
        while (i < k){
            char tem = s[i];
            s[i] = s[k];
            s[k] = tem;
            i ++;
            k --;
        }
    }
}

//With a char[], you can swap characters directly with O(1) extra memory.
class Solution {
    public String reverseStr(String s, int k) {
        char[] arr = s.toCharArray();
        int n = arr.length;
        for(int start = 0; start < n; start += 2*k){
            int i = start;
            int j = start + k - 1;
            while(i<j){
                char tem = arr[i];
                arr[i] = arr[j];
                arr[j] = tem;
                i++;
                j--;
            }
        }
        return new String(arr);
    }
}

//https://leetcode.com/problems/reverse-vowels-of-a-string/
class Solution {
    public String reverseVowels(String s) {
        char[] arrs = s.toCharArray();
        int s_index = 0;
        int e_index = arrs.length-1;
        while(s_index < e_index){
            if(ifVowels(arrs[s_index])){
                if(ifVowels(arrs[e_index])){
                    char tem = arrs[s_index];
                    arrs[s_index] = arrs[e_index];
                    arrs[e_index] = tem;
                    s_index++;
                    e_index--;
                }else{
                    e_index--;
                }
            }else{
                s_index++;
            }
        }
        return new String(arrs);
    }

    public boolean ifVowels(char s) {
        char c = Character.toLowerCase(s);
        if(c == 'a' || c == 'e' || c == 'i' || c == 'o' || c == 'u' ){
            return true;
        }
        return false;
    }
}

//https://leetcode.com/problems/reverse-words-in-a-string-iii/
class Solution {
    public String reverseWords(String s) {
        String[] arr = s.trim().split("\\s+");
        StringBuilder sb = new StringBuilder();
        for (int i=0;i<arr.length;i++){
            char[] char_arr = arr[i].toCharArray();
            int n =0;
            int m = char_arr.length-1;
            while(n<m){
                char tem = char_arr[n];
                char_arr[n] = char_arr[m];
                char_arr[m] = tem;
                n++;
                m--;
            }
            sb.append(char_arr);
            if( i != arr.length-1){
                sb.append(" ");
            }
        }
        return sb.toString();
    }
}