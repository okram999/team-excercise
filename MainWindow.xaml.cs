using System;
using System.Collections.ObjectModel;
using System.DirectoryServices.AccountManagement;
using System.Windows;
using System.Windows.Input;
using Amazon.Connect;
using Amazon.ConnectParticipant;

namespace AnyStateITSupport
{
    public partial class MainWindow : Window
    {
        private ObservableCollection<ChatMessage> _messages = new ObservableCollection<ChatMessage>();
        private string _currentUser;
        private AmazonConnectClient _connectClient;
        private AmazonConnectParticipantClient _participantClient;
        private string _contactId;
        private string _participantToken;
        private bool _isConnectedToLiveAgent = false;

        public MainWindow()
        {
            InitializeComponent();
            ChatMessages.ItemsSource = _messages;
            
            // Get current Windows user
            GetCurrentUser();
            
            // Initialize Amazon Connect client
            InitializeConnectClient();
            
            // Add welcome message
            AddSystemMessage("Welcome to AnyState IT Support. How can I help you today?");
        }

        private void GetCurrentUser()
        {
            try
            {
                // Get current Windows user from domain
                using (var context = new PrincipalContext(ContextType.Domain))
                {
                    var user = UserPrincipal.Current;
                    _currentUser = user.DisplayName;
                    UserInfoText.Text = $"Welcome, {_currentUser}";
                }
            }
            catch (Exception)
            {
                // Fallback if domain authentication fails
                _currentUser = Environment.UserName;
                UserInfoText.Text = $"Welcome, {_currentUser}";
            }
        }

        private void InitializeConnectClient()
        {
            try
            {
                _connectClient = new AmazonConnectClient();
                _participantClient = new AmazonConnectParticipantClient();
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Error connecting to Amazon Connect: {ex.Message}", "Connection Error", MessageBoxButton.OK, MessageBoxImage.Error);
            }
        }

        private void SendButton_Click(object sender, RoutedEventArgs e)
        {
            SendMessage();
        }

        private void MessageInput_KeyDown(object sender, KeyEventArgs e)
        {
            if (e.Key == Key.Enter && !Keyboard.Modifiers.HasFlag(ModifierKeys.Shift))
            {
                SendMessage();
                e.Handled = true;
            }
        }

        private void SendMessage()
        {
            string message = MessageInput.Text.Trim();
            if (string.IsNullOrEmpty(message))
                return;

            // Add user message to chat
            AddUserMessage(message);
            
            // Clear input
            MessageInput.Clear();
            
            // Process message
            if (_isConnectedToLiveAgent)
            {
                // Send to live agent via Connect
                SendMessageToLiveAgent(message);
            }
            else
            {
                // Process with AI
                ProcessWithAI(message);
            }
        }

        private void AddUserMessage(string message)
        {
            _messages.Add(new ChatMessage
            {
                SenderName = _currentUser,
                Message = message,
                Timestamp = DateTime.Now.ToString("h:mm tt"),
                IsUser = true
            });
        }

        private void AddSystemMessage(string message)
        {
            _messages.Add(new ChatMessage
            {
                SenderName = "IT Support",
                Message = message,
                Timestamp = DateTime.Now.ToString("h:mm tt"),
                IsUser = false
            });
        }

        private void ProcessWithAI(string message)
        {
            // Simulate AI processing
            // In a real implementation, this would call Amazon Lex or another AI service
            
            string response;
            
            if (message.ToLower().Contains("password reset"))
            {
                response = "To reset your password, please visit the self-service portal at https://reset.anystate.gov or call the IT helpdesk at 555-123-4567.";
            }
            else if (message.ToLower().Contains("software") || message.ToLower().Contains("install"))
            {
                response = "For software installation requests, please use the Software Request form in the Employee Portal. An IT technician will review and process your request.";
            }
            else if (message.ToLower().Contains("vpn") || message.ToLower().Contains("remote"))
            {
                response = "For VPN access or remote connectivity issues, please ensure you're using the latest AnyState VPN client. For installation instructions, visit https://vpn.anystate.gov";
            }
            else
            {
                response = "I'm not sure I understand your question. Would you like to speak with a live IT support agent?";
            }
            
            // Add AI response to chat
            AddSystemMessage(response);
        }

        private void LiveAgentButton_Click(object sender, RoutedEventArgs e)
        {
            ConnectToLiveAgent();
        }

        private void ConnectToLiveAgent()
        {
            try
            {
                // In a real implementation, this would initiate a chat with Amazon Connect
                AddSystemMessage("Connecting you to a live agent. Please wait a moment...");
                
                // Simulate connection delay
                // In production, this would be an async call to Amazon Connect
                _isConnectedToLiveAgent = true;
                
                AddSystemMessage("You are now connected with a live agent. Please note that live agent support is available Monday to Friday, 9 AM to 5 PM.");
                LiveAgentButton.IsEnabled = false;
            }
            catch (Exception ex)
            {
                AddSystemMessage($"Error connecting to live agent: {ex.Message}");
                _isConnectedToLiveAgent = false;
            }
        }

        private void SendMessageToLiveAgent(string message)
        {
            // In a real implementation, this would send the message to Amazon Connect
            // For this demo, we'll simulate a response
            
            // Simulate agent typing delay
            AddSystemMessage("Agent is typing...");
            
            // In production, this would be handled by the actual agent response
            AddSystemMessage("Thank you for your message. An IT support specialist will assist you shortly.");
        }

        private void CallbackButton_Click(object sender, RoutedEventArgs e)
        {
            RequestCallback();
        }

        private void RequestCallback()
        {
            // Show callback dialog
            var dialog = new CallbackRequestWindow();
            if (dialog.ShowDialog() == true)
            {
                string phoneNumber = dialog.PhoneNumber;
                
                // In a real implementation, this would schedule a callback via Amazon Connect
                AddSystemMessage($"A callback has been scheduled to {phoneNumber}. An IT support specialist will call you shortly during business hours (Monday to Friday, 9 AM to 5 PM).");
            }
        }
    }

    public class ChatMessage
    {
        public string SenderName { get; set; }
        public string Message { get; set; }
        public string Timestamp { get; set; }
        public bool IsUser { get; set; }
    }
}