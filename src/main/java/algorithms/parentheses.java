//https://leetcode.com/problems/valid-parentheses/
class Solution {
    public boolean isValid(String s) {
        char[] c = s.toCharArray();
        Stack<Character> s_stack = new Stack();
        for(int i=0;i<c.length;i++){
            if(c[i]=='('|| c[i]=='{'|| c[i]=='['){
                s_stack.push(c[i]);
            }else{
                if(s_stack.isEmpty()){
                    return false;
                }else{
                    char s_c = s_stack.pop();
                    if( s_c =='(' && c[i] != ')'){
                        return false;
                    } else if( s_c =='{' && c[i] != '}'){
                        return false;
                    }else if( s_c =='[' && c[i] != ']'){
                        return false;
                    }
                }
            }
        }
        if(c.length <= 0){
            return false;
        }else{
            return true;
        }
    }
}

//https://leetcode.com/problems/minimum-add-to-make-parentheses-valid/
class Solution {
    public int minAddToMakeValid(String s) {
        char[] c = s.toCharArray();
        Stack<Character> s_stack = new Stack();
        int min=0;
        for (int i=0;i<c.length;i++){
            if(c[i]=='('|| c[i]=='{'|| c[i]=='['){
                s_stack.push(c[i]);
            }else{
                if(s_stack.isEmpty()){
                    min++;
                }else{
                    char s_c = s_stack.pop();
                    if( s_c =='(' && c[i] != ')'){
                        min++;
                    } else if( s_c =='{' && c[i] != '}'){
                        min++;
                    }else if( s_c =='[' && c[i] != ']'){
                        min++;
                    }
                }
                
            }
        }
        if(c.length==s_stack.size()){
            min+=s_stack.size();
        }
        return min;
    }
}

//https://leetcode.com/problems/remove-outermost-parentheses/
class Solution {
    public String removeOuterParentheses(String s) {
        char[] c = s.toCharArray();
        int balance = 0;
        StringBuilder sb = new StringBuilder();
        for (int i=0;i<c.length;i++){
            char tem_c = c[i];
            if(tem_c == '('){
                if(balance > 0 ){
                    sb.append(tem_c);
                }
                balance++;
            }else{
                 balance--;
                 if(balance > 0 ){
                    sb.append(tem_c);
                }
            }
        }
        return sb.toString();
    }
}