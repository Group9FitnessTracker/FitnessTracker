package bubble;

import java.util.*;


public class Statistician 
{
	private final static int N_REPETITIONS = 1000;
	
	
	//returns a array of random integers with values between -maxValue and maxValue
	private static int[] buildRandom(int length, int maxValue)
	{
		int[] array = new int[length];
		for (int i=0; i<length; i++)
			array[i] = (int)(Math.random()*(maxValue + 1));
		return array;
	}
	
	private static boolean isSorted(int[] a) {
		for(int i=0;i<a.length-1;i++) {
			if(a[i]>a[i+1]) {return false;}
		}
		return true;
	}
	
	private static void getStats(int arrayLength)
	{
		ArrayList<Long> visitCounts = new ArrayList<>();
		ArrayList<Long> swapCounts = new ArrayList<>();
		
		for (int i=0; i<N_REPETITIONS; i++)
		{
			int[] array = buildRandom(arrayLength, arrayLength*100);
			BubbleSorter sorter = new BubbleSorter(array);
			sorter.sort();
			// Assert that the sorter sorted correctly.
			if(!isSorted(sorter.getArray())) {
				System.out.println("not sorted!");
			}
			assert(isSorted(sorter.getArray())):"no sorty!";
			// Append # visits and # swaps to the array lists.
			visitCounts.add(sorter.getNVisits());
			swapCounts.add(sorter.getNSwaps());

		}

		// Compute and print min/average/max number of visits.
		long minVisit = Collections.min(visitCounts);
		long maxVisit = Collections.max(visitCounts);	
		long totalVisit = 0;
		for(Long visitCount:visitCounts) {
			totalVisit += visitCount;
		}
		double avgVisit = totalVisit/N_REPETITIONS;
		System.out.println("MinVist: " +minVisit+" maxVisit: "+maxVisit+" avgVisit:"+ avgVisit);
		
		
		// Compute and print min/average/max number of swaps.
		long minSwaps = Collections.min(swapCounts);
		long maxSwaps = Collections.max(visitCounts);
		long totalSwaps = 0;
		for(Long swapCount:swapCounts) {
			totalSwaps += swapCount;
		}
		double avgSwap = totalSwaps/N_REPETITIONS;
		System.out.println("MinSwap: " +minSwaps+" maxSwap: "+maxSwaps+" avgSwap:"+ avgSwap);


	}
	
	public static void main(String[] args)
	{
		int[] tiny = {1,24,5,25};
		int[] alreadySorted = {1,2,3,4,5};//fill in your example
		int[] backward = {5,4,3,2,1};//fill in your example
		System.out.println("Tiny");
		BubbleSorter tinySorted = new BubbleSorter(tiny);
		tinySorted.sort();
		System.out.println(tinySorted);
		
		System.out.println("Already Sorted");
		BubbleSorter alrSorted = new BubbleSorter(alreadySorted);
		alrSorted.sort();
		System.out.println(alrSorted);
		
		System.out.println("Backward");
		BubbleSorter b = new BubbleSorter(backward);
		b.sort();
		System.out.println(b);
	
        System.out.println("1000:");
        getStats(1000);
        
        
		System.out.println("3000:");
		getStats(3000);
		
	}
}
