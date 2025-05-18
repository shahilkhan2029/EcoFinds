<?php
require_once "../config.php";

$success_msg = $error_msg = "";

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Get form data
    $name = trim($_POST["name"]);
    $email = trim($_POST["email"]);
    $phone = trim($_POST["phone"]);
    $service_type = trim($_POST["service_type"]);
    $message = trim($_POST["message"]);
    $preferred_date = trim($_POST["preferred_date"]);
    $preferred_time = trim($_POST["preferred_time"]);

    // Insert into database
    $sql = "INSERT INTO legal_consultations (name, email, phone, service_type, message, preferred_date, preferred_time, status) 
            VALUES (?, ?, ?, ?, ?, ?, ?, 'Pending')";
    
    if($stmt = mysqli_prepare($conn, $sql)){
        mysqli_stmt_bind_param($stmt, "sssssss", 
            $name, $email, $phone, $service_type, 
            $message, $preferred_date, $preferred_time);
        
        if(mysqli_stmt_execute($stmt)){
            $success_msg = "Your consultation request has been submitted successfully! Our legal team will contact you within 24 hours.";
        } else{
            $error_msg = "Error submitting request. Please try again.";
        }
        mysqli_stmt_close($stmt);
    }
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Legal Services | PrimeHomes</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Arial', sans-serif;
        }

        body {
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
        }

        .main-header-content {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .logo {
            display: flex;
            align-items: center;
            gap: 10px;
            text-decoration: none;
            color: #2c3e50;
        }

        .logo i {
            font-size: 24px;
            color: #007bff;
        }

        .logo h1 {
            font-size: 24px;
            font-weight: bold;
            color: #FF6B6B;
        }

        .main-nav {
            display: flex;
            gap: 40px;
            align-items: center;
        }

        .nav-link {
            text-decoration: none;
            color: #2c3e50;
            font-weight: 500;
            padding: 8px 0;
            position: relative;
            transition: color 0.3s ease;
        }

        .nav-link:hover {
            color: #007bff;
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

        .nav-link:hover::after,
        .nav-link.active::after {
            width: 100%;
        }

        .nav-link.active {
            color: #007bff;
        }

        .dropdown-btn {
            text-decoration: none;
            color: white;
            font-weight: 500;
            padding: 8px 15px;
            background: #007bff;
            border-radius: 4px;
            display: flex;
            align-items: center;
            gap: 5px;
            transition: all 0.3s ease;
        }

        .dropdown-btn:hover {
            background: #0056b3;
        }

        /* Main Content Styles */
        .container {
            max-width: 1200px;
            margin: 40px auto;
            padding: 0 20px;
        }

        .service-header {
            text-align: center;
            margin-bottom: 40px;
        }

        .service-header h2 {
            font-size: 2.5rem;
            color: #2c3e50;
            margin-bottom: 15px;
        }

        .service-header p {
            color: #666;
            font-size: 1.1rem;
            max-width: 800px;
            margin: 0 auto;
        }

        .services-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
            margin: 60px 0;
        }

        .service-card {
            background: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            text-align: center;
        }

        .service-card i {
            font-size: 40px;
            color: #007bff;
            margin-bottom: 20px;
        }

        .service-card h3 {
            color: #2c3e50;
            margin-bottom: 15px;
        }

        .service-card p {
            color: #666;
            line-height: 1.6;
        }

        .consultation-form {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }

        .form-group {
            margin-bottom: 20px;
        }

        .form-group label {
            display: block;
            margin-bottom: 5px;
            color: #2c3e50;
            font-weight: 500;
        }

        .form-control {
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 14px;
        }

        .form-control:focus {
            outline: none;
            border-color: #007bff;
        }

        textarea.form-control {
            height: 120px;
            resize: vertical;
        }

        .submit-btn {
            background: #007bff;
            color: white;
            padding: 12px 30px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
            width: 100%;
            transition: background 0.3s ease;
        }

        .submit-btn:hover {
            background: #0056b3;
        }

        .alert {
            padding: 15px;
            margin-bottom: 20px;
            border-radius: 4px;
        }

        .alert-success {
            background-color: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }

        .alert-danger {
            background-color: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }

        .time-slots {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }
    </style>
</head>
<body>
    <!-- Header -->
    <header class="main-header">
        <div class="main-header-content">
            <a href="../index.php" class="logo">
                <i class="fas fa-home"></i>
                <h1>PrimeHomes</h1>
            </a>
            <nav class="main-nav">
                <a href="../index.php" class="nav-link">Home</a>
                <a href="../rent.php" class="nav-link">Rent</a>
                <a href="../sell.php" class="nav-link">Sell</a>
                <a href="../contact.php" class="nav-link">Contact</a>
                <a href="../add-property.php" class="dropdown-btn">
                    <i class="fas fa-plus"></i> Add Property
                </a>
            </nav>
        </div>
    </header>

    <div class="container">
        <div class="service-header">
            <h2>Legal Services</h2>
            <p>Expert legal assistance for all your real estate needs. Our team of experienced attorneys provides comprehensive legal services to protect your interests.</p>
        </div>

        <div class="services-grid">
            <div class="service-card">
                <i class="fas fa-file-contract"></i>
                <h3>Contract Review</h3>
                <p>Thorough review and analysis of real estate contracts, purchase agreements, and lease documents.</p>
            </div>
            <div class="service-card">
                <i class="fas fa-search-location"></i>
                <h3>Title Search</h3>
                <p>Comprehensive title search and verification to ensure clear property ownership.</p>
            </div>
            <div class="service-card">
                <i class="fas fa-handshake"></i>
                <h3>Closing Services</h3>
                <p>Professional assistance throughout the closing process, including document preparation and review.</p>
            </div>
            <div class="service-card">
                <i class="fas fa-gavel"></i>
                <h3>Legal Consultation</h3>
                <p>Expert advice on real estate laws, regulations, and dispute resolution.</p>
            </div>
            <div class="service-card">
                <i class="fas fa-building"></i>
                <h3>Property Disputes</h3>
                <p>Resolution of property-related disputes, boundary issues, and tenant-landlord conflicts.</p>
            </div>
            <div class="service-card">
                <i class="fas fa-shield-alt"></i>
                <h3>Legal Protection</h3>
                <p>Comprehensive legal protection for your real estate investments and transactions.</p>
            </div>
        </div>

        <div class="consultation-form">
            <h3 style="text-align: center; margin-bottom: 30px; color: #2c3e50;">Schedule a Consultation</h3>
            
            <?php 
            if(!empty($success_msg)){
                echo '<div class="alert alert-success">' . $success_msg . '</div>';
            }
            if(!empty($error_msg)){
                echo '<div class="alert alert-danger">' . $error_msg . '</div>';
            }
            ?>

            <form action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]); ?>" method="POST">
                <div class="form-group">
                    <label>Full Name</label>
                    <input type="text" name="name" class="form-control" required>
                </div>

                <div class="form-group">
                    <label>Email Address</label>
                    <input type="email" name="email" class="form-control" required>
                </div>

                <div class="form-group">
                    <label>Phone Number</label>
                    <input type="tel" name="phone" class="form-control" required>
                </div>

                <div class="form-group">
                    <label>Service Type</label>
                    <select name="service_type" class="form-control" required>
                        <option value="">Select Service Type</option>
                        <option value="contract_review">Contract Review</option>
                        <option value="title_search">Title Search</option>
                        <option value="closing_services">Closing Services</option>
                        <option value="legal_consultation">Legal Consultation</option>
                        <option value="property_disputes">Property Disputes</option>
                        <option value="legal_protection">Legal Protection</option>
                    </select>
                </div>

                <div class="form-group">
                    <label>Message</label>
                    <textarea name="message" class="form-control" placeholder="Please describe your legal needs or concerns..."></textarea>
                </div>

                <div class="time-slots">
                    <div class="form-group">
                        <label>Preferred Date</label>
                        <input type="date" name="preferred_date" class="form-control" required min="<?php echo date('Y-m-d'); ?>">
                    </div>

                    <div class="form-group">
                        <label>Preferred Time</label>
                        <select name="preferred_time" class="form-control" required>
                            <option value="">Select Time</option>
                            <option value="09:00">9:00 AM</option>
                            <option value="10:00">10:00 AM</option>
                            <option value="11:00">11:00 AM</option>
                            <option value="13:00">1:00 PM</option>
                            <option value="14:00">2:00 PM</option>
                            <option value="15:00">3:00 PM</option>
                            <option value="16:00">4:00 PM</option>
                        </select>
                    </div>
                </div>

                <button type="submit" class="submit-btn">Schedule Consultation</button>
            </form>
        </div>
    </div>
</body>
</html> 