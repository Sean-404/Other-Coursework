
public abstract class Transaction {
    private int accountNo;
    // protected int accountNo;

    private Screen screen;
    private BankDatabase database;

    public Transaction(int accountNo, Screen screen, BankDatabase database) {
        this.accountNo = accountNo;
        this.screen = screen;
        this.database = database;
    }

    // method would not be needed if account no was protected
    public int getAccountNo() {
        return accountNo;
    }

    // public method not discovered in design stage
    public Screen getScreen() {
        return screen;
    }

    // public method not discovered in design stage
    public BankDatabase getBankDatabase() {
        return database;
    }

    public abstract void execute();
    // {

    // }
}
