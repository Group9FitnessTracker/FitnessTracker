package birds;

public class Swan extends Bird{
	public void glide() {
		System.out.println("I'm Graceful");
	}
	public static void main(String [] args) {
		Bird duck = new Duck();
		Swan s = new Swan();
		
		Bird b = (Swan)s;
		
		Duck d = (Duck)b;//Fixed by casting: RHS type = Duck, LHS type =
				//Duck, RHS is superclass of LHS
		Duck d1 = (Duck)duck;//Fixed by casting: RHS type = Duck, LHS type =
		//Duck, RHS is superclass of LHS
		d1.quack();
		d.quack(); //swan, cannot quack
		
	}

}
