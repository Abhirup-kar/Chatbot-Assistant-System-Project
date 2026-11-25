from django.core.management.base import BaseCommand

from assistant.models import TechGuide


GUIDES_DATA = [
    {
        'slug': 'python-installation-setup',
        'title': 'Install & Configure Python & PATH',
        'category': TechGuide.CATEGORY_SETUP,
        'summary': (
            'To install Python cleanly, download the latest stable installer for your OS, '
            'enable "Add python.exe to PATH" during Windows installation, and verify the '
            'interpreter and pip inside a virtual environment.'
        ),
        'keywords': (
            'python, install python, python setup, path, environment variable, '
            'python not recognized, pip not found, venv, virtual environment, python3'
        ),
        'sample_questions': [
            'How do I install Python and add it to PATH?',
            'Why is python not recognized in terminal?',
        ],
        'external_url': 'https://docs.python.org/3/using/index.html',
        'external_label': 'Official Python Setup & Usage Docs',
        'steps_json': [
            {
                'heading': 'Download the official installer',
                'detail': 'Get the latest Python 3 release from python.org or your OS package manager.',
                'command': 'python3 --version',
            },
            {
                'heading': 'Enable PATH on Windows',
                'detail': 'Check "Add python.exe to PATH" on the first screen of the Windows setup wizard before clicking Install Now.',
                'command': 'where python',
            },
            {
                'heading': 'Create an isolated virtual environment',
                'detail': 'Always isolate project dependencies using venv inside your project folder.',
                'command': 'python3 -m venv .venv && source .venv/bin/activate',
            },
            {
                'heading': 'Verify pip and package installation',
                'detail': 'Upgrade pip inside the activated virtual environment so packages install cleanly.',
                'command': 'python -m pip install --upgrade pip',
            },
        ],
    },
    {
        'slug': 'django-project-setup',
        'title': 'Set Up a Django Web Application',
        'category': TechGuide.CATEGORY_DEVTOOLS,
        'summary': (
            'Setting up Django involves creating a virtual environment, installing Django via pip, '
            'running startproject and startapp, applying initial database migrations, and starting '
            'the local development server.'
        ),
        'keywords': (
            'django, setup django, django project, startproject, startapp, runserver, '
            'migrations, makemigrations, migrate, web application, python web framework'
        ),
        'sample_questions': [
            'How do I set up a Django project?',
            'How do I run Django migrations and start the server?',
        ],
        'external_url': 'https://docs.djangoproject.com/en/stable/intro/tutorial01/',
        'external_label': 'Official Django Getting Started Tutorial',
        'steps_json': [
            {
                'heading': 'Install Django inside a virtual environment',
                'detail': 'Activate your virtual environment and install Django.',
                'command': 'pip install django',
            },
            {
                'heading': 'Create project and app',
                'detail': 'Initialize the Django project directory and create your first application module.',
                'command': 'django-admin startproject myproject . && python manage.py startapp core',
            },
            {
                'heading': 'Register the app and migrate',
                'detail': 'Add your app name to INSTALLED_APPS in settings.py, then apply database migrations.',
                'command': 'python manage.py makemigrations && python manage.py migrate',
            },
            {
                'heading': 'Start the development server',
                'detail': 'Launch the local server and open http://127.0.0.1:8000/ in your browser.',
                'command': 'python manage.py runserver',
            },
        ],
    },
    {
        'slug': 'xampp-mysql-setup',
        'title': 'Install & Configure XAMPP / MySQL Server & Fix Port Conflicts',
        'category': TechGuide.CATEGORY_SETUP,
        'summary': (
            'XAMPP bundles Apache and MySQL/MariaDB for local development. If Apache or MySQL fails '
            'to start, check for port 80/443 or 3306 conflicts, run the Control Panel as administrator, '
            'and configure phpMyAdmin or Django database credentials.'
        ),
        'keywords': (
            'xampp, xamp, mysql, mariadb, apache, phpmyadmin, port 80, port 3306, '
            'mysql shutdown unexpectedly, xampp server, xampp setup, apache not starting'
        ),
        'sample_questions': [
            'How do I install and configure XAMPP server?',
            'MySQL or Apache in XAMPP fails to start due to port conflict.',
        ],
        'external_url': 'https://www.apachefriends.org/faq_windows.html',
        'external_label': 'XAMPP Official Documentation & FAQ',
        'steps_json': [
            {
                'heading': 'Install XAMPP in a clean root directory',
                'detail': 'Install XAMPP to C:\\xampp (or /opt/lampp on Linux) to avoid Windows UAC permission blocks.',
                'command': '',
            },
            {
                'heading': 'Resolve Apache port 80/443 conflicts',
                'detail': 'In XAMPP Control Panel click Config -> httpd.conf and change Listen 80 to Listen 8080 if another service occupies port 80.',
                'command': 'netstat -ano | findstr :80',
            },
            {
                'heading': 'Fix MySQL port 3306 or unexpected shutdown',
                'detail': 'Stop conflicting local MySQL services or update my.ini port from 3306 to 3307; restore backup folder only if InnoDB logs are corrupted.',
                'command': 'netstat -ano | findstr :3306',
            },
            {
                'heading': 'Create a database in phpMyAdmin',
                'detail': 'Open http://localhost/phpmyadmin, create a UTF8MB4 database, and verify host/user/password settings.',
                'command': 'CREATE DATABASE chatbot_assistant_db CHARACTER SET utf8mb4;',
            },
        ],
    },
    {
        'slug': 'git-github-setup',
        'title': 'Git & GitHub Setup and SSH Configuration',
        'category': TechGuide.CATEGORY_DEVTOOLS,
        'summary': (
            'Configure Git with your name and email, generate an Ed25519 SSH key for passwordless '
            'GitHub authentication, and verify your remote connection before pushing code.'
        ),
        'keywords': (
            'git, github, ssh key, git config, git push, repository, clone, merge conflict, '
            'permission denied publickey, version control'
        ),
        'sample_questions': [
            'How do I set up Git and SSH keys for GitHub?',
            'How do I fix GitHub permission denied publickey?',
        ],
        'external_url': 'https://docs.github.com/en/authentication/connecting-to-github-with-ssh',
        'external_label': 'GitHub SSH Setup Documentation',
        'steps_json': [
            {
                'heading': 'Set global Git identity',
                'detail': 'Configure your commit author name and email once on your machine.',
                'command': 'git config --global user.name "Your Name" && git config --global user.email "you@example.com"',
            },
            {
                'heading': 'Generate an Ed25519 SSH key',
                'detail': 'Create a new SSH key pair and add it to the ssh-agent.',
                'command': 'ssh-keygen -t ed25519 -C "you@example.com"',
            },
            {
                'heading': 'Add the public key to GitHub and test',
                'detail': 'Copy ~/.ssh/id_ed25519.pub into GitHub Settings -> SSH and GPG keys, then test authentication.',
                'command': 'ssh -T git@github.com',
            },
        ],
    },
    {
        'slug': 'vscode-python-setup',
        'title': 'Configure VS Code & Sublime Text for Python Development',
        'category': TechGuide.CATEGORY_DEVTOOLS,
        'summary': (
            'Configure your editor to use the project virtual environment interpreter, enable syntax '
            'linting and auto-formatting, and set up an integrated run/debug configuration.'
        ),
        'keywords': (
            'vscode, vs code, sublime text, editor, ide, python interpreter, pylance, '
            'import could not be resolved, linting, debugger, code editor setup'
        ),
        'sample_questions': [
            'How do I configure VS Code for Python and Django?',
            'Why does VS Code say import django could not be resolved?',
        ],
        'external_url': 'https://code.visualstudio.com/docs/python/python-tutorial',
        'external_label': 'VS Code Python Getting Started Guide',
        'steps_json': [
            {
                'heading': 'Install the Python extension',
                'detail': 'Install Microsoft Python extension in VS Code (or Package Control + LSP in Sublime Text).',
                'command': 'code --install-extension ms-python.python',
            },
            {
                'heading': 'Select the virtual environment interpreter',
                'detail': 'Open the Command Palette (Ctrl+Shift+P), run "Python: Select Interpreter", and pick .venv/bin/python.',
                'command': '',
            },
            {
                'heading': 'Verify integrated terminal activation',
                'detail': 'Open a new terminal in the editor and confirm which/where python points inside .venv.',
                'command': 'which python',
            },
        ],
    },
    {
        'slug': 'wifi-network-troubleshooting',
        'title': 'Fix Wi-Fi & Internet Connectivity Issues',
        'category': TechGuide.CATEGORY_NETWORK,
        'summary': (
            'Most Wi-Fi and DNS dropouts are resolved by flushing the DNS cache, renewing your DHCP '
            'IP lease, resetting the network adapter stack, and testing connectivity with ping.'
        ),
        'keywords': (
            'wifi, wi-fi, internet, network, no internet, dns, dhcp, ipconfig, ping, '
            'connected no internet, slow internet, router, ethernet, network adapter'
        ),
        'sample_questions': [
            'My Wi-Fi says connected with no internet, how do I fix it?',
            'How do I flush DNS and reset my network connection?',
        ],
        'external_url': 'https://support.microsoft.com/en-us/windows/fix-wi-fi-connection-issues-in-windows-9424a1f7-6a3b-65a6-4d78-7f07eee84d2c',
        'external_label': 'Microsoft Wi-Fi Troubleshooting Guide',
        'steps_json': [
            {
                'heading': 'Test gateway and external reachability',
                'detail': 'Check whether your computer can reach an external IP vs. resolve domain names.',
                'command': 'ping 8.8.8.8',
            },
            {
                'heading': 'Flush DNS and renew IP address (Windows)',
                'detail': 'Run Command Prompt as Administrator to clear stale DNS entries and renew your IP lease.',
                'command': 'ipconfig /flushdns && ipconfig /release && ipconfig /renew',
            },
            {
                'heading': 'Reset Winsock / TCP/IP stack if needed',
                'detail': 'If websites still fail to load, reset network sockets and reboot your PC and router.',
                'command': 'netsh winsock reset',
            },
        ],
    },
    {
        'slug': 'slow-pc-performance',
        'title': 'Fix Slow Computer & High CPU/RAM Usage',
        'category': TechGuide.CATEGORY_OS,
        'summary': (
            'Speed up a sluggish PC by identifying heavy processes in Task Manager or System Monitor, '
            'disabling unnecessary startup apps, freeing disk space (keep 15%+ free on SSD), and '
            'checking disk health.'
        ),
        'keywords': (
            'slow pc, slow computer, high cpu, high ram, high memory, 100 disk, '
            'lagging, freezing, startup apps, task manager, performance, sluggish'
        ),
        'sample_questions': [
            'Why is my computer running so slow?',
            'How do I fix 100% disk or high CPU usage?',
        ],
        'external_url': 'https://support.microsoft.com/en-us/windows/tips-to-improve-pc-performance-in-windows-b3b3ef5b-5953-fb6a-2528-4bbed82fba96',
        'external_label': 'Official PC Performance Optimization Tips',
        'steps_json': [
            {
                'heading': 'Inspect top CPU, RAM, and Disk consumers',
                'detail': 'Open Task Manager (Ctrl+Shift+Esc) or htop/System Monitor and sort by CPU or Memory to spot runaway apps.',
                'command': 'htop',
            },
            {
                'heading': 'Disable heavy startup programs',
                'detail': 'In Task Manager -> Startup apps, disable non-essential updaters and chat clients from launching at boot.',
                'command': '',
            },
            {
                'heading': 'Free temporary files and check storage',
                'detail': 'Ensure your OS drive has at least 15-20 GB free space and run Disk Cleanup or Storage Sense.',
                'command': 'cleanmgr',
            },
        ],
    },
    {
        'slug': 'blue-screen-bsod-fix',
        'title': 'Troubleshoot Blue Screen (BSOD) & System Crashes',
        'category': TechGuide.CATEGORY_OS,
        'summary': (
            'Blue Screen (BSOD) and kernel crashes usually stem from faulty drivers, recent updates, '
            'corrupted system files, or failing RAM. Boot into Safe Mode, run SFC/DISM integrity checks, '
            'and roll back recently updated drivers.'
        ),
        'keywords': (
            'bsod, blue screen, crash, system crash, kernel panic, stop code, '
            'unexpected reboot, safe mode, sfc, dism, driver crash'
        ),
        'sample_questions': [
            'How do I fix a Blue Screen (BSOD) error?',
            'My PC keeps crashing and restarting randomly.',
        ],
        'external_url': 'https://support.microsoft.com/en-us/windows/resolving-blue-screen-errors-in-windows-60b01860-58f2-be66-7516-5c45a66ae3c6',
        'external_label': 'Resolving Blue Screen Errors Guide',
        'steps_json': [
            {
                'heading': 'Note the Stop Code and boot to Safe Mode',
                'detail': 'Record the error code (e.g. DRIVER_IRQL_NOT_LESS_OR_EQUAL) and start in Safe Mode if crashes loop.',
                'command': '',
            },
            {
                'heading': 'Repair system files with DISM and SFC',
                'detail': 'Open an elevated terminal and verify Windows system image and file integrity.',
                'command': 'DISM /Online /Cleanup-Image /RestoreHealth && sfc /scannow',
            },
            {
                'heading': 'Check hardware memory and recent drivers',
                'detail': 'Roll back any newly installed GPU/chipset driver and run Windows Memory Diagnostic (mdsched.exe).',
                'command': 'mdsched.exe',
            },
        ],
    },
    {
        'slug': 'audio-sound-not-working',
        'title': 'Fix Audio Output & Microphone Problems',
        'category': TechGuide.CATEGORY_HARDWARE,
        'summary': (
            'Fix missing sound or microphone input by verifying the active default playback/recording '
            'device, checking OS microphone privacy permissions, restarting the audio service, and '
            'reinstalling the audio driver.'
        ),
        'keywords': (
            'audio, sound, no sound, speaker, headphones, microphone, mic not working, '
            'volume, audio driver, realtek, pulseaudio, pipewire'
        ),
        'sample_questions': [
            'Why is there no sound coming from my speakers or headphones?',
            'My microphone is not working in calls.',
        ],
        'external_url': 'https://support.microsoft.com/en-us/windows/fix-sound-or-audio-problems-in-windows-73025246-b61c-40fb-671a-2535c5cd56c8',
        'external_label': 'Official Audio Troubleshooting Guide',
        'steps_json': [
            {
                'heading': 'Verify the default output and input device',
                'detail': 'Open Sound Settings and make sure your speakers/headset (not an unused monitor HDMI output) are set as default.',
                'command': 'mmsys.cpl',
            },
            {
                'heading': 'Check app microphone permissions',
                'detail': 'Ensure Privacy & Security -> Microphone allows desktop and browser access.',
                'command': '',
            },
            {
                'heading': 'Restart the audio service or update driver',
                'detail': 'Restart Windows Audio in services.msc (or restart pipewire/pulseaudio on Linux).',
                'command': 'systemctl --user restart pipewire pipewire-pulse',
            },
        ],
    },
    {
        'slug': 'bluetooth-pairing-issues',
        'title': 'Fix Bluetooth Connection & Pairing Issues',
        'category': TechGuide.CATEGORY_HARDWARE,
        'summary': (
            'Resolve Bluetooth pairing failures by removing stale device profiles, toggling Bluetooth '
            'and Airplane mode off/on, ensuring the accessory is in discovery mode, and restarting the '
            'Bluetooth Support Service.'
        ),
        'keywords': (
            'bluetooth, pairing, bluetooth not connecting, wireless headphones, '
            'bluetooth missing, device not found, disconnect, bluetooth driver'
        ),
        'sample_questions': [
            'My Bluetooth headphones will not pair or keep disconnecting.',
            'Bluetooth toggle disappeared from settings.',
        ],
        'external_url': 'https://support.microsoft.com/en-us/windows/fix-bluetooth-problems-in-windows-723e092f-03fa-858b-5c80-131ec3fba75c',
        'external_label': 'Official Bluetooth Troubleshooting Guide',
        'steps_json': [
            {
                'heading': 'Remove old pairing records',
                'detail': 'Forget/remove the device on both your PC and phone so they do not hijack the connection.',
                'command': '',
            },
            {
                'heading': 'Put accessory into fresh pairing mode',
                'detail': 'Hold the pairing button until the LED flashes rapidly, then add the device in Bluetooth settings.',
                'command': '',
            },
            {
                'heading': 'Restart Bluetooth service or adapter',
                'detail': 'Restart the Bluetooth Support Service (or bluetoothd on Linux) and update the wireless driver.',
                'command': 'sudo systemctl restart bluetooth',
            },
        ],
    },
    {
        'slug': 'printer-setup-troubleshooting',
        'title': 'Set Up Printer & Fix Print Spooler Errors',
        'category': TechGuide.CATEGORY_HARDWARE,
        'summary': (
            'Set up a USB or Wi-Fi printer by connecting it to the same subnet as your PC, installing '
            'manufacturer drivers, and clearing stuck jobs by restarting the Print Spooler service.'
        ),
        'keywords': (
            'printer, print spooler, printer offline, cannot print, setup printer, '
            'wifi printer, print queue stuck, scanner, cups'
        ),
        'sample_questions': [
            'How do I set up a wireless printer?',
            'My printer says offline or the print queue is stuck.',
        ],
        'external_url': 'https://support.microsoft.com/en-us/windows/fix-printer-connection-and-printing-problems-in-windows-fb830bff-770f-6349-33cd-9443fe987f73',
        'external_label': 'Official Printer Setup & Troubleshooting Guide',
        'steps_json': [
            {
                'heading': 'Confirm network or USB connection',
                'detail': 'Ensure the printer and PC share the same Wi-Fi network (not a guest network) or reconnect the USB cable directly.',
                'command': '',
            },
            {
                'heading': 'Clear stuck print queue and restart Spooler',
                'detail': 'Stop the Spooler service, clear C:\\Windows\\System32\\spool\\PRINTERS, and restart the service.',
                'command': 'net stop spooler && net start spooler',
            },
            {
                'heading': 'Add printer by IP if discovery fails',
                'detail': 'Print a network configuration page from the printer and add it via TCP/IP port in Printers & Scanners.',
                'command': '',
            },
        ],
    },
    {
        'slug': 'windows-update-errors',
        'title': 'Fix OS & Windows Update Failures',
        'category': TechGuide.CATEGORY_OS,
        'summary': (
            'Fix stuck or failing OS updates by ensuring 20 GB of free disk space, running the Update '
            'Troubleshooter, clearing the SoftwareDistribution cache, and verifying system files.'
        ),
        'keywords': (
            'windows update, os update, update failed, stuck update, update error, '
            'softwaredistribution, apt update, system update'
        ),
        'sample_questions': [
            'Windows Update keeps failing or getting stuck.',
            'How do I reset update components?',
        ],
        'external_url': 'https://support.microsoft.com/en-us/windows/troubleshoot-problems-updating-windows-188c2b0f-10a7-d72f-65b8-32d177eb136c',
        'external_label': 'Official OS Update Troubleshooting Guide',
        'steps_json': [
            {
                'heading': 'Check storage and disconnect extra USB drives',
                'detail': 'Free at least 20 GB on the system drive and unplug non-essential external storage.',
                'command': '',
            },
            {
                'heading': 'Reset Windows Update services and cache',
                'detail': 'Stop wuauserv and bits, rename SoftwareDistribution, and restart services.',
                'command': 'net stop wuauserv && net stop bits && net start bits && net start wuauserv',
            },
            {
                'heading': 'Repair Linux packages if on Ubuntu/Debian',
                'detail': 'If updating a Linux system, fix interrupted dpkg configurations and refresh package lists.',
                'command': 'sudo dpkg --configure -a && sudo apt update && sudo apt upgrade',
            },
        ],
    },
    {
        'slug': 'browser-slow-cache-fix',
        'title': 'Fix Slow Browser, Crashes & SSL/Cache Errors',
        'category': TechGuide.CATEGORY_NETWORK,
        'summary': (
            'Resolve slow page loads, stale UI states, and HTTPS certificate warnings by clearing '
            'cached site data, disabling conflicting extensions, verifying system clock accuracy, '
            'and updating your browser.'
        ),
        'keywords': (
            'browser, chrome, firefox, edge, slow browser, clear cache, cookies, '
            'ssl error, your connection is not private, extension crash, page not loading'
        ),
        'sample_questions': [
            'How do I fix a slow browser or clear cache and cookies?',
            'Why am I seeing an SSL connection not private error?',
        ],
        'external_url': 'https://support.google.com/chrome/answer/95669',
        'external_label': 'Chrome Connection & Cache Help',
        'steps_json': [
            {
                'heading': 'Test in an Incognito/Private window',
                'detail': 'Open a private tab to quickly verify whether an extension or corrupted cookie is causing the issue.',
                'command': '',
            },
            {
                'heading': 'Clear cached images, files, and site cookies',
                'detail': 'Open Browser Settings -> Privacy and Security -> Clear browsing data for the affected site.',
                'command': '',
            },
            {
                'heading': 'Verify date & time for SSL/HTTPS errors',
                'detail': 'An inaccurate system clock breaks TLS certificates; turn on automatic time sync.',
                'command': 'timedatectl status',
            },
        ],
    },
    {
        'slug': 'database-connection-errors',
        'title': 'Troubleshoot SQLite/MySQL Connection & Migration Errors',
        'category': TechGuide.CATEGORY_DEVTOOLS,
        'summary': (
            'Database errors in Python/Django usually come from unapplied migrations, locked SQLite '
            'files, wrong MySQL credentials, or a stopped database server. Verify service status, '
            'inspect settings.py DATABASES, and run migrate.'
        ),
        'keywords': (
            'database, sqlite, mysql, migration, operationalerror, no such table, '
            'access denied, connection refused, db error, database locked'
        ),
        'sample_questions': [
            'How do I fix Django OperationalError no such table?',
            'Why is MySQL refusing connection or access denied?',
        ],
        'external_url': 'https://docs.djangoproject.com/en/stable/topics/migrations/',
        'external_label': 'Django Migrations & Database Docs',
        'steps_json': [
            {
                'heading': 'Apply pending Django migrations',
                'detail': 'If you see "OperationalError: no such table", generate and apply migrations.',
                'command': 'python manage.py makemigrations && python manage.py migrate',
            },
            {
                'heading': 'Verify MySQL service and credentials',
                'detail': 'Confirm MySQL/MariaDB is running on port 3306 and test login with the exact host and user configured in settings.py.',
                'command': 'mysql -u root -h 127.0.0.1 -P 3306 -p',
            },
            {
                'heading': 'Inspect migration state',
                'detail': 'Use showmigrations to see which migrations are applied or pending.',
                'command': 'python manage.py showmigrations',
            },
        ],
    },
    {
        'slug': 'email-account-setup',
        'title': 'Set Up IMAP/SMTP Email Client & Fix Login Errors',
        'category': TechGuide.CATEGORY_NETWORK,
        'summary': (
            'Configure desktop or mobile email clients using encrypted IMAP (port 993 SSL/TLS) and '
            'SMTP (port 465 SSL or 587 STARTTLS), and use an App Password if 2-Factor Authentication '
            'is enabled on your account.'
        ),
        'keywords': (
            'email, imap, smtp, outlook, thunderbird, gmail setup, app password, '
            'cannot send email, email authentication failed, port 587, port 993'
        ),
        'sample_questions': [
            'How do I set up IMAP and SMTP email in Outlook or Thunderbird?',
            'Why does my email client reject my password?',
        ],
        'external_url': 'https://support.google.com/mail/answer/7126229',
        'external_label': 'IMAP & SMTP Configuration Reference',
        'steps_json': [
            {
                'heading': 'Enable IMAP in webmail settings',
                'detail': 'Verify IMAP access is enabled in your email provider account settings.',
                'command': '',
            },
            {
                'heading': 'Use standard encrypted ports',
                'detail': 'Set Incoming IMAP to port 993 (SSL/TLS) and Outgoing SMTP to port 587 (STARTTLS) or 465 (SSL/TLS).',
                'command': '',
            },
            {
                'heading': 'Generate an App Password when 2FA is active',
                'detail': 'If your provider uses 2-step verification, generate a dedicated App Password instead of using your main login password.',
                'command': '',
            },
        ],
    },
    {
        'slug': 'malware-security-cleanup',
        'title': 'PC Security, Password Safety & Malware Cleanup',
        'category': TechGuide.CATEGORY_SECURITY,
        'summary': (
            'Protect your system against malware and suspicious popups by running a full antivirus '
            'scan, removing unknown browser extensions, updating your OS, and enabling two-factor '
            'authentication with unique passwords.'
        ),
        'keywords': (
            'malware, virus, antivirus, security, popup, adware, hack, phishing, '
            'two factor, 2fa, firewall, defender, suspicious'
        ),
        'sample_questions': [
            'How do I remove malware or suspicious popups from my PC?',
            'How should I secure my accounts after a suspicious login?',
        ],
        'external_url': 'https://support.microsoft.com/en-us/windows/stay-protected-with-windows-security-2ae0363d-0ada-c064-8b56-6a39afb6a963',
        'external_label': 'Windows Security & Malware Protection Guide',
        'steps_json': [
            {
                'heading': 'Run a full or offline security scan',
                'detail': 'Disconnect from untrusted networks if needed and run a Full Scan or Offline Scan in Windows Security.',
                'command': '',
            },
            {
                'heading': 'Audit installed programs and browser extensions',
                'detail': 'Uninstall unfamiliar apps and remove unknown browser extensions causing redirects or popups.',
                'command': '',
            },
            {
                'heading': 'Rotate passwords and enable 2FA',
                'detail': 'Change compromised passwords from a clean device and enable Two-Factor Authentication.',
                'command': '',
            },
        ],
    },
]


def ensure_knowledge_base_seeded() -> tuple[int, int]:
    """Idempotently seed all technical guides into the database."""
    created_count = 0
    updated_count = 0
    for item in GUIDES_DATA:
        _, created = TechGuide.objects.update_or_create(
            slug=item['slug'],
            defaults={
                'title': item['title'],
                'category': item['category'],
                'summary': item['summary'],
                'steps_json': item['steps_json'],
                'keywords': item['keywords'],
                'sample_questions': item['sample_questions'],
                'external_url': item['external_url'],
                'external_label': item['external_label'],
            },
        )
        if created:
            created_count += 1
        else:
            updated_count += 1
    return created_count, updated_count


class Command(BaseCommand):
    help = 'Seeds the technical troubleshooting and setup knowledge base.'

    def handle(self, *args, **options):
        created, updated = ensure_knowledge_base_seeded()
        total = TechGuide.objects.count()
        self.stdout.write(
            self.style.SUCCESS(
                f'Knowledge base seeded: {created} created, {updated} updated ({total} total guides).'
            )
        )
