//https://leetcode.com/problems/two-sum/
class Solution {
    public int[] twoSum(int[] nums, int target) {
        int[] result_array = new int[2];
        for(int i=0;i<nums.length;i++){
            for(int j=i+1;j<nums.length;j++){
                if(nums[i]+nums[j]==target){
                    result_array[0]=i;
                    result_array[1]=j;
                }
            }
        }
        return result_array;
    }
}

class Solution {
    public int[] twoSum(int[] nums, int target) {
        Map<Integer, Integer> result_map = new HashMap<>();
        int[] arry = new int[2];
        for (int i=0;i<nums.length;i++){
            int v = target-nums[i];
            if(result_map.containsKey(v)){
                arry[0]=result_map.get(v);
                arry[1]=i;
                return arry;
            }
            result_map.put(nums[i],i);
        }
        return arry;

    }
}