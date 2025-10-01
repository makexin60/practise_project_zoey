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