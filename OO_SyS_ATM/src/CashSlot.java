
public class CashSlot {
    private final int START_NO = 500; // not going to change so declare as final
    private int count;

    public CashSlot() {
        count = START_NO;
    }

    public void dispenseCash(int amount) {
        int notes = amount / 20;
        count -= notes;
    }

    public boolean isSufficientCashAvailable(int amount) {
        int notes = amount / 20;

        if (count >= notes) {
            return true;
        }
        else {
            return false;
        }
    }
}
