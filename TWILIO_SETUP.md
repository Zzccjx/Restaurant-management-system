# Twilio SMS Integration Setup Guide

This guide will help you set up Twilio SMS to send OTP codes to users' mobile numbers.

## Prerequisites

1. A Twilio account (free trial available)
2. Python 3.8+ installed
3. The project dependencies installed

## Step 1: Install Twilio Package

The Twilio package is already included in `requirements.txt`. Install it by running:

```bash
pip install -r requirements.txt
```

Or install Twilio directly:

```bash
pip install twilio
```

## Step 2: Create Twilio Account

1. **Sign up for Twilio:**
   - Go to https://www.twilio.com/try-twilio
   - Sign up for a free account (no credit card required for trial)

2. **Verify your account:**
   - Twilio will send a verification code to your phone
   - Enter the code to verify your account

## Step 3: Get Twilio Credentials

1. **Log in to Twilio Console:**
   - Go to https://www.twilio.com/console

2. **Get Account SID:**
   - On the dashboard, you'll see your "Account SID"
   - Copy this value (starts with "AC...")

3. **Get Auth Token:**
   - Click on "Auth Token" in the dashboard
   - Click "View" to reveal your Auth Token
   - Copy this value (keep it secret!)

4. **Get Phone Number:**
   - Go to "Phone Numbers" → "Manage" → "Buy a number"
   - Or use the trial number provided (format: +1234567890)
   - Copy the phone number in E.164 format (e.g., +1234567890)

## Step 4: Configure Environment Variables

1. **Copy the example file:**
   ```bash
   # Windows PowerShell
   Copy-Item .env.example .env
   
   # Linux/Mac
   cp .env.example .env
   ```

2. **Edit the .env file:**
   Open `.env` in a text editor and fill in your Twilio credentials:

   ```env
   TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   TWILIO_AUTH_TOKEN=your_auth_token_here
   TWILIO_PHONE_NUMBER=+1234567890
   ```

   Replace:
   - `ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx` with your Account SID
   - `your_auth_token_here` with your Auth Token
   - `+1234567890` with your Twilio phone number

3. **Save the file**

## Step 5: Test the Integration

1. **Restart your Flask application:**
   ```bash
   python app.py
   ```

2. **Test OTP sending:**
   - Go to the login page
   - Enter a mobile number
   - Click "Send OTP"
   - Check your phone for the SMS with the OTP code

## Troubleshooting

### OTP Not Received

1. **Check Twilio Console:**
   - Go to https://www.twilio.com/console/logs/sms
   - Check if SMS was sent and if there are any errors

2. **Verify Phone Number Format:**
   - Phone numbers must be in E.164 format: `+[country code][number]`
   - Example: `+919876543210` for India, `+1234567890` for US

3. **Check Trial Account Limits:**
   - Free trial accounts can only send SMS to verified phone numbers
   - Verify your phone number in Twilio Console → Phone Numbers → Verified Caller IDs

4. **Check Environment Variables:**
   - Make sure `.env` file exists and has correct values
   - Restart the application after changing `.env`

### Error: "Twilio not installed"

```bash
pip install twilio
```

### Error: "Invalid credentials"

- Double-check your Account SID and Auth Token
- Make sure there are no extra spaces in `.env` file
- Restart the application

### Development Mode (No SMS)

If you don't want to use SMS (for development):
- Don't set the Twilio environment variables
- Or leave them empty in `.env`
- OTP will be displayed on the login page instead

## Twilio Trial Account Limitations

- **Verified Numbers Only:** Free trial can only send SMS to verified phone numbers
- **Limited Credits:** Trial account has limited credits
- **Upgrade for Production:** For production use, upgrade your Twilio account

## Production Deployment

For production:

1. **Upgrade Twilio Account:**
   - Upgrade from trial to paid account
   - Add payment method

2. **Secure Environment Variables:**
   - Never commit `.env` file to version control
   - Use secure environment variable management (AWS Secrets Manager, etc.)

3. **Monitor Usage:**
   - Set up billing alerts in Twilio Console
   - Monitor SMS usage and costs

## Alternative SMS Providers

If you prefer other SMS providers, you can modify `utils/auth.py`:

- **AWS SNS:** Amazon Simple Notification Service
- **TextLocal:** Popular in India
- **MSG91:** Another Indian SMS provider
- **Vonage (formerly Nexmo):** International SMS provider

## Support

- **Twilio Documentation:** https://www.twilio.com/docs
- **Twilio Support:** https://support.twilio.com
- **Project Issues:** Check the project repository for issues
