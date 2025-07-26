# 📱 India Salary Calculator - Mobile App

A mobile application built using **KivyMD** that calculates the **annual and monthly salary breakdown** as per **India's New Tax Regime** for the **financial year 2025-26**.

---

## 📌 Features

- **Touch-friendly Material Design UI** with cards and smooth scrolling
- Enter your **Annual CTC** and get instant calculations:
  - Employee PF deductions
  - Standard deductions  
  - Taxable income
  - Income tax (with health & education cess)
  - Final **in-hand salary** (monthly & yearly)

- **Quick Set Buttons**: 10 LPA, 20 LPA, 50 LPA for instant CTC setting
- **Error handling** with user-friendly dialogs
- **Responsive design** that works on phones and tablets

---

## 🛠️ Technologies Used

| Technology | Purpose |
|------------|---------|
| **Python 3.x** | Core programming language |
| **KivyMD** | Material Design UI framework |
| **Kivy** | Cross-platform GUI framework |
| **Buildozer** | Android APK packaging tool |

---

## 🚀 Installation & Setup

### 📋 Prerequisites

- **Python 3.7+** installed on your system
- **pip** package manager
- For Android builds: **Java JDK**, **Android SDK**, **NDK**

### 🔧 Local Development Setup

1. **Navigate to the mobile app directory:**
   ```bash
   cd "Screenshots/Mob App"
   ```

2. **Install required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the mobile app:**
   ```bash
   python mobile_salary_calculator.py
   ```

The app will open in a desktop window for testing and development.

---

## 📱 Building for Android

### 🏗️ Build APK (Debug)

1. **Install Buildozer:**
   ```bash
   pip install buildozer
   ```

2. **Initialize Buildozer (first time only):**
   ```bash
   buildozer init
   ```

3. **Build debug APK:**
   ```bash
   buildozer android debug
   ```

4. **Install on connected Android device:**
   ```bash
   buildozer android debug install run
   ```

### 🚀 Build Release APK

1. **Build release APK:**
   ```bash
   buildozer android release
   ```

2. **Sign the APK** (requires keystore):
   ```bash
   jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 -keystore my-release-key.keystore bin/*.apk alias_name
   ```

---

## 📂 Project Structure

```
Screenshots/Mob App/
├── mobile_salary_calculator.py    # Main mobile app code
├── requirements.txt               # Python dependencies
├── buildozer.spec                # Android build configuration
└── README.md                     # This documentation
```

---

## 🧮 Tax Calculation Logic

The mobile app uses the **same calculation logic** as the desktop version:

- **New Tax Regime** slabs for FY 2025–26
- Assumes **Basic + DA = 50% of CTC**
- PF calculated at **12% of Basic + DA** (capped at ₹15,000/month)
- **Standard Deduction**: ₹75,000
- **87A Rebate**: ₹60,000 for income ≤ ₹12,00,000
- **Health & Education Cess**: 4% on tax

---

## 🎨 UI Components

### Main Screen Elements:
- **Title Header**: App name and tax regime info
- **CTC Input Field**: Numeric input with validation
- **Quick Set Buttons**: 10 LPA, 20 LPA, 50 LPA
- **Calculate Button**: Triggers salary breakdown
- **Results Cards**: Scrollable annual and monthly breakdowns

### Material Design Features:
- **Elevated Cards** for result display
- **Primary Color Theming** (Blue)
- **Touch Ripple Effects** on buttons
- **Error Dialogs** with proper messaging

---

## 🔧 Troubleshooting

### Common Issues:

**1. Import Error: No module named 'kivymd'**
```bash
pip install kivymd kivy
```

**2. Buildozer fails on first run:**
```bash
# Install system dependencies (Ubuntu/Debian)
sudo apt update
sudo apt install -y git zip unzip openjdk-8-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev

# For other systems, check Buildozer documentation
```

**3. APK not installing on device:**
- Enable **Developer Options** and **USB Debugging**
- Allow **Install from Unknown Sources**
- Check device compatibility (Android 5.0+)

**4. App crashes on Android:**
- Check `buildozer.spec` requirements
- Ensure all dependencies are listed
- Test on desktop first

---

## 📱 Device Compatibility

- **Minimum Android Version**: 5.0 (API 21)
- **Target Android Version**: 13 (API 33)
- **Architecture Support**: ARM64, ARMv7
- **Screen Sizes**: Phone and Tablet optimized

---

## 🚀 Development Commands

| Command | Purpose |
|---------|---------|
| `python mobile_salary_calculator.py` | Run app locally |
| `buildozer android debug` | Build debug APK |
| `buildozer android release` | Build release APK |
| `buildozer android clean` | Clean build files |
| `buildozer android logcat` | View device logs |

---

## 📄 Build Configuration

The `buildozer.spec` file contains:
- **App metadata** (name, version, package)
- **Python requirements** (kivy, kivymd)
- **Android permissions** (if needed)
- **Build settings** (architecture, API levels)

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Test on both desktop and Android
4. Submit a pull request

---

## 📧 Support

For issues or questions:
- **Email**: senkvarghese316@gmail.com
- **GitHub Issues**: Create an issue in the repository

---

## 📄 License

This project is open source under the [MIT License](https://opensource.org/licenses/MIT).

---

**Happy Calculating! 💰📱**