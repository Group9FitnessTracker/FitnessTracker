package dotlab;
import java.io.*;
public class DotReader
{
	private BufferedReader br;
	public DotReader(BufferedReader br){
		this.br = br;
	}
	
	public Dot readDot() throws IOException,DotException{
		DotException de = new DotException("Invalid Input");
		String line = br.readLine();
		if(line == null)return null;
		String[] values = line.split(",");
		if(values.length != 4) throw de;
		String color = values[0];
		int x = Integer.parseInt(values[1]);
		int y = Integer.parseInt(values[2]);
		int radius = Integer.parseInt(values[3]);
		
		return new Dot(color,x,y,radius);
		
		
	}
}