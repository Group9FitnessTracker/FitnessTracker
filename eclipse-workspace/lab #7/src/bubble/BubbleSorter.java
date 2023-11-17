package bubble;

public class BubbleSorter 
{
	private int[]		a;
	private long		nVisits;
	private long		nSwaps;
	
	
	public BubbleSorter(int[] a)
	{
		this.a = a; 
	}
	
	
	public void sort()
	{
		nVisits = 0;
		nSwaps = 0;
		int n = a.length;
		boolean swapped;
		for(int i = n-1;i>=0;i--) {
			swapped = false;
			for(int j = n-1;j>n-i-1;j--) {
				nVisits += 2;
				if(a[j]<a[j-1]) {
					int temp = a[j];
					a[j] = a[j-1];
					a[j-1] = temp;
					nSwaps++;
					nVisits += 4;
					swapped = true;
				}
			}
			if(!swapped) { //already sorted if no swaps
				break;
			}
		}
		
		
		
	}
	
	
	public String toString()
	{
		String s = nVisits + " visits, " + nSwaps + " swaps\n{";
		for (int n: a)
			s += " " + n;
		s += " }";
		return s;
	}
	
	public long getNVisits()
	{
		return nVisits;
	}
	
	
	public long getNSwaps()
	{
		return nSwaps;
	}
	
	
	public int[] getArray()
	{
		return a;
	}
	
	
	
}
