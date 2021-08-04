import java.util.Scanner;

// whole class merely wraps input as an emulated keypad
public class KeyPad {
	private Scanner s;
	
    public KeyPad() {
    	s = new Scanner(System.in);
    }

    public int getInput() {
        return s.nextInt();
    }
}
