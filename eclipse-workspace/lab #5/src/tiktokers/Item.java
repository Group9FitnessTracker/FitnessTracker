package tiktokers;

public class Item
{
    private String username;
    private String key;
    private String value;

    public String getKey()
    {
        return key;
    }

    public String getUserName()
    {
        return username;
    }

    public String getValue()
    {
        return value;
    }

    public Item(String username, String key, String value)
    {
        this.username = username;
        this.key = key;
        this.value = value;
    }

    public void setValue(String value)
    {
        this.value = value;
    }
}

