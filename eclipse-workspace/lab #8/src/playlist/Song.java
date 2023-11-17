package playlist;

public class Song {
	
	private String title;
	private String artist;
	
	public Song(String title, String artist) {
		this.title = title;
		this.artist = artist;
	}
	@Override
	public boolean equals(Object obj) {
		Song s = (Song)obj;
		return title.equals(s.title) && artist.equals(s.artist);
	}
	
	@Override
	public int hashCode() {
		return title.hashCode()+artist.hashCode();
	}
	
	@Override
	public String toString() {
		return title + " by " + artist;
	}
	
	public String getArtist() {
		return artist;
	}
	
	public String getTitle() {
		return title;
	}
	
	public void setArtist(String artist) {
		this.artist = artist;
	}
	
	public void setTitle(String title) {
		this.title = title;
	}
	

}
