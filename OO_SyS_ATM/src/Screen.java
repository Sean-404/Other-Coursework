
// whole class merely wraps output as an emulated screen
public class Screen {
    public Screen() {

    }

    public void displayMessage(String message) {
        System.out.print(message);
    }

    public void displayMessageLine(String message) {
    	System.out.println(message);
    }

    public void displayAmount(double amount) {
        System.out.format("£%,.2f", amount);
    }
}
