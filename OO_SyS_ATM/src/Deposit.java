
public class Deposit extends Transaction {
    private double amount;
    private KeyPad keyPad;
    private DepositSlot depositSlot;

    private final int ABORT = 0;

    public Deposit(int accountNo, Screen screen, BankDatabase database, KeyPad keyPad, DepositSlot depositSlot) {
    	super(accountNo, screen, database);

        this.keyPad = keyPad;
        this.depositSlot = depositSlot;
    }

    @Override
    public void execute() {
        Screen screen = getScreen();
        BankDatabase database = getBankDatabase();

        amount = promptDepositAmount();

        if (amount != ABORT) {
            screen.displayMessageLine("");
            screen.displayMessage("Please insert deposit envelope that contains : ");
            screen.displayAmount(amount);
            screen.displayMessageLine("");

            boolean envelopeReceive = depositSlot.isEnvelopeReceive();

            if (envelopeReceive) {
                screen.displayMessageLine("");
                screen.displayMessageLine("Your envelope has been receive.");
                screen.displayMessageLine("NOTE: The money deposited will not be available until we verify the enclosed cash.");

                database.credit(getAccountNo(), amount);
                // database.credit(accountNo, amount);
            }
            else {
                screen.displayMessageLine("");
                screen.displayMessageLine("You did not insert an envelope, so the ATM has aborted your transaction.");
            }
        }
        else  {
            screen.displayMessageLine("");
            screen.displayMessageLine("Aborting Transaction . .");
        }
    }

    private double promptDepositAmount() {
        Screen screen = getScreen();

        screen.displayMessageLine("");
        screen.displayMessage("Please enter a deposit amount in PENCE (or 0 to abort) : ");

        int input = keyPad.getInput();

        if (input == ABORT) {
            return ABORT;
        }
        else {
            return (double)input/100.0;
        }
    }
}
