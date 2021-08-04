
public final class Account {
    private int accountNo;
    private int pin;
    private double availableBalance;
    private double totalBalance;

    public Account(int accountNo, int pin, double availableBalance, double totalBalance) {
        this.accountNo = accountNo;
        this.pin = pin;
        this.availableBalance = availableBalance;
        this.totalBalance = totalBalance;
    }

    public boolean validatePIN(int userPIN) {
        if (pin == userPIN) {
            return true;
        }
        else {
            return false;
        }

        // return false;
    }

    public double getAvailableBalance() {
        return availableBalance;
    }

    public double getTotalBalance() {
        return totalBalance;
    }

    public void credit(double amount) {
        totalBalance += amount;
    }

    public void debit(double amount) {
        availableBalance -= amount;
        totalBalance -= amount;
    }

    // public method not discovered in design stage
    public int getAccountNo() {
        return accountNo;
    }
}
