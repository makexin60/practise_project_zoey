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

//https://leetcode.com/problems/valid-palindrome-ii/
class Solution {
    public boolean validPalindrome(String s) {
        char[] c = s.toCharArray();
        int i=0;
        int j=c.length-1;
        while(i<j){
            if(c[i]!=c[j]){
                return validCharPalindrome(c,i+1,j)||validCharPalindrome(c,i,j-1);
            }
            i++;
            j--;
        }
        return true;
    }
    public boolean validCharPalindrome(char[] s,int left,int right){
        while(left<right){
            if(s[left]!=s[right]){
                return false;
            }
            left++;
            right--;
        }
        return true;
    }
}

//https://leetcode.com/problems/longest-palindrome/
class Solution {
    public int longestPalindrome(String s) {
        int[] count = new int[128];
        char[] c = s.toCharArray();
        int max=0;
        boolean hasOdd = false;
        for (int i=0;i<c.length;i++){
            count[c[i]]++;
        }
        for(int j=0;j<count.length;j++){
            if(count[j]>0){
                if(count[j]%2==0){
                    max+=count[j];
                }else if(count[j]==1){
                    if(!hasOdd){
                        max+=1;
                        hasOdd = true;
                    }
                }else{
                    int tem=count[j]-1;
                    max+=tem;
                }
            }
        }
        return max;
    }
}