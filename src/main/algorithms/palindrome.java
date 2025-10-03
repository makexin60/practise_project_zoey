//https://leetcode.com/problems/valid-palindrome/
class Solution {
    public boolean isPalindrome(String s) {
        char[] c = s.toCharArray();
        int i = 0;
        int j = c.length-1;
        while(i<j){
            while(i<j && !Character.isLetterOrDigit(c[i])){
                i++;
            }
            while(i<j && !Character.isLetterOrDigit(c[j])){
                j--;
            }
            if(Character.toLowerCase(c[i])!=Character.toLowerCase(c[j])){
                return false;
            }
            i++;
            j--;
        }
        return true;
    }
}

//