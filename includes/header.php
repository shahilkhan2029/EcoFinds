<?php
require_once('../config.php');
$current_page = isset($current_page) ? $current_page : '';
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PrimeHomes</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        /* Global Styles */
        :root {
            --primary: #4a6fa5;
            --secondary: #166088;
            --accent: #4fc3f7;
            --light: #f8f9fa;
            --dark: #343a40;
            --success: #28a745;
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }

        body {
            min-height: 100vh;
            background-color: #f5f5f5;
        }

        /* Header Styles */
        .main-header {
            background-color: white;
            padding: 20px 0;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            position: sticky;
            top: 0;
            z-index: 1000;
            transition: all 0.3s ease;
        }

        .main-header:hover {
            box-shadow: 0 4px 15px rgba(0,0,0,0.15);
        }

        .main-header-content {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            transition: all 0.3s ease;
        }

        .logo {
            display: flex;
            align-items: center;
            gap: 10px;
            text-decoration: none;
            color: #2c3e50;
            transition: transform 0.3s ease;
        }

        .logo:hover {
            transform: scale(1.05);
        }

        .logo i {
            font-size: 24px;
            color: #007bff;
            transition: color 0.3s ease;
        }

        .logo:hover i {
            color: #0056b3;
        }

        .logo h1 {
            font-size: 24px;
            font-weight: bold;
            color: #FF6B6B;
            margin: 0;
        }

        .main-nav {
            display: flex;
            gap: 30px;
            align-items: center;
        }

        .nav-link {
            text-decoration: none;
            color: #2c3e50;
            font-weight: 500;
            padding: 8px 0;
            position: relative;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            gap: 5px;
        }

        .nav-link i {
            font-size: 16px;
        }

        .nav-link::after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 0;
            width: 0;
            height: 2px;
            background-color: #007bff;
            transition: width 0.3s ease;
        }

        .nav-link:hover {
            color: #007bff;
        }

        .nav-link:hover::after,
        .nav-link.active::after {
            width: 100%;
        }

        .nav-link.active {
            color: #007bff;
        }
    </style>
</head>
<body>
    <header class="main-header">
        <div class="main-header-content">
            <a href="../index.php" class="logo">
                <i class="fas fa-home"></i>
                <h1>PrimeHomes</h1>
            </a>
            <nav class="main-nav">
                <a href="../index.php" class="nav-link <?php echo $current_page === 'home' ? 'active' : ''; ?>">
                    <i class="fas fa-home"></i> Home
                </a>
                <a href="../rent.php" class="nav-link <?php echo $current_page === 'rent' ? 'active' : ''; ?>">
                    <i class="fas fa-key"></i> Rent
                </a>
                <a href="../sell.php" class="nav-link <?php echo $current_page === 'sell' ? 'active' : ''; ?>">
                    <i class="fas fa-tag"></i> Sell
                </a>
                <a href="../contact.php" class="nav-link <?php echo $current_page === 'contact' ? 'active' : ''; ?>">
                    <i class="fas fa-envelope"></i> Contact
                </a>
            </nav>
        </div>
    </header>
</body>
</html> 