//https://leetcode.com/problems/binary-search/
class Solution {
    public int search(int[] nums, int target) {
        int left = 0;
        int right = nums.length;
        while(left<=right){
            int mid = left + (right-left)/2;
            if(nums[mid]==target){
                return mid;
            }else if(nums[mid]<target){
                left = mid +1;
            }else if(nums[mid]>target){
                right = mid -1;
            }
        }
        return -1;
    }
}

//https://leetcode.com/problems/search-insert-position/
class Solution {
    public int searchInsert(int[] nums, int target) {
        int left =0;
        int right = nums.length-1;
        while(left<=right){
            int mid = left +(right-left)/2;
            if(nums[mid]==target){
                return mid;
            }else if(nums[mid]<target){
                left = mid+1;
            }else if(nums[mid]>target){
                right = mid-1;
            }
        }
        return left;

    }
}

//https://leetcode.com/problems/word-search/
class Solution {
    public boolean exist(char[][] board, String word) {
        int m = board.length;
        int n = board[0].length;

        for (int i=0;i<m;i++){
            for(int j=0;j<n;j++){
                if(board[i][j]==word.charAt(0)&&dns(board,word,i,j,0)){
                    return true;
                }
            }
        }
        return false;
    }

    public boolean dns(char[][] board,String word,int i,int j,int index){

        if(index==word.length()){
            return true;
        }
        
        if(i<0||j<0||i>board.length-1||j>board[0].length-1||board[i][j]!=word.charAt(index)){
            return false;
        }

        char tem = board[i][j];
        board[i][j]= '#';

        boolean flag_result =dns(board,word,i-1,j,index+1)||
        dns(board,word,i,j-1,index+1)||
        dns(board,word,i+1,j,index+1)||
        dns(board,word,i,j+1,index+1);

        board[i][j]=tem;

        return flag_result;
    }
}

	      `·

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

//https://leetcode.com/problems/validate-binary-search-tree/
/**
 * Definition for a binary tree node.
 * public class TreeNode {
 *     int val;
 *     TreeNode left;
 *     TreeNode right;
 *     TreeNode() {}
 *     TreeNode(int val) { this.val = val; }
 *     TreeNode(int val, TreeNode left, TreeNode right) {
 *         this.val = val;
 *         this.left = left;
 *         this.right = right;
 *     }
 * }
 */
class Solution {
    public boolean isValidBST(TreeNode root) {
        return isSubtree(root,Long.MIN_VALUE,Long.MAX_VALUE);
    }

    public boolean isSubtree(TreeNode node, long min, long max){
        if(node==null){
            return true;
        }
        if(node.val<=min || node.val >=max){
            return false;
        }
        return isSubtree(node.left,min,node.val)&&isSubtree(node.right,node.val,max);
    }
}