if [ ! -d "venv" ]; then
    source install.sh
fi

source venv/scripts/activate
echo "Running..."
python telegram_bot.py
