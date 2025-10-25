//https://leetcode.com/problems/find-pivot-index/
class Solution {
    public int pivotIndex(int[] nums) {
        int total_sum = 0;
        for(int num : nums){
            total_sum+=num;
        }

        int left_sum = 0;
        for(int i=0;i<nums.length;i++){
            if(left_sum == total_sum - nums[i]- left_sum){
                return i;
            }
            left_sum+=nums[i];
        }
        return -1;
    }

}