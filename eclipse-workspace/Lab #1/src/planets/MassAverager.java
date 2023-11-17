package planets;

public class MassAverager
{
	// Complete this. Retrieve the array of planets, then compute average mass.
	Planet[] arrayPlanets = Planet.getAll();
	public float getMeanPlanetaryMass()
	{
		
		float total = 0.0f;
		for(int i = 0;i<arrayPlanets.length;i++) {
			total += arrayPlanets[i].getMass();
		}
		return total/arrayPlanets.length;
	}
		
	//
	// In almost all classes in almost all 46B homework assignments, the main()
	// method is for you to test your code. The autograder doesn't look at the
	// output from main().
	//
	// Since this assignment is simple, there's really only 1 useful version of
	// main(), and you can fill it in here. Later, when your assignments are more
	// complicated, your main() will change several or many times as you develop
	// different pieces of your assignment. It also serves as a great place to writ
	// test cases. Later in the semester, we will learn even more ways to guarantee
	// your code is correct
	public static void main(String[] args)
	{
		MassAverager averager = new MassAverager();
		System.out.println(averager.getMeanPlanetaryMass()); //test case
		
		
	}
}
