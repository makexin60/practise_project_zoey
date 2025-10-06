//https://leetcode.com/problems/string-to-integer-atoi/
class Solution {
    public int myAtoi(String s) {
        String ss =s.trim();
        int results =0;
        if (ss.isEmpty()){
            return results;
        }else{
            char[] c = ss.toCharArray();
            int i =0;
            int sign = 1;
            int min = -2^31;
            int max = 2^31-1;
            if (c[i]=='-'||c[i]=='+') {
                sign = c[i] == '-' ?-1:1;
                i++;
            } else if (!Character.isDigit(c[i])){
                return results;
            }

            while (i < c.length && Character.isDigit(c[i])) {
                results = results * 10 + (c[i] - '0');
                if(sign*results<Integer.MIN_VALUE){
                    return Integer.MIN_VALUE;
                }
                if(sign*results>Integer.MAX_VALUE){
                    return Integer.MAX_VALUE;
                }
                i++;
            }
            return sign*results;
        }
    }
}