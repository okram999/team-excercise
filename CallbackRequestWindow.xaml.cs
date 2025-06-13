using System.Windows;

namespace AnyStateITSupport
{
    public partial class CallbackRequestWindow : Window
    {
        public string PhoneNumber { get; private set; }
        
        public CallbackRequestWindow()
        {
            InitializeComponent();
        }
        
        private void RequestButton_Click(object sender, RoutedEventArgs e)
        {
            if (string.IsNullOrWhiteSpace(PhoneNumberInput.Text))
            {
                MessageBox.Show("Please enter a valid phone number.", "Invalid Input", MessageBoxButton.OK, MessageBoxImage.Warning);
                return;
            }
            
            PhoneNumber = PhoneNumberInput.Text;
            DialogResult = true;
            Close();
        }
        
        private void CancelButton_Click(object sender, RoutedEventArgs e)
        {
            DialogResult = false;
            Close();
        }
    }
}