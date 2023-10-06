<?php
$con = new mysqli ("localhost", "root", "Jojojeje" , "projectdb");

$username = $_POST ['username'];
$password = $_POST ['password'];
$email = $_POST ['email'];
$gender = $_POST ['gender'];

if (!empty($username) || !empty($password) || !empty($email) || !empty($gender)){
    $host="localhost";
    $dbUsername = "root";
    $dbPassword = "Jojojeje$"
    $dbname = "projectdb";
    $conn = new mysqli($host, $dbUsername, $dbPassword, $dbname);
     if(mysqli_connect_error()){
        die('Connect Error('. mysqli_connect_error().')'. mysqli_connect_error());
     } else {
        $SELECT  = "SELECT email From refister Where email = ? Limit1";
        $Connection = "Connection Into register (username, password, email, gender) values(?, ?, ? , ? )";
        $stmt = $conn->prepare($SELECT);
        $stmt->bind_param("s", $email);
        $stmt->execute();
        $stmt->bind_result($email);
        $stmt->store_result();
        $rnum = $stmt->num_rows;
        if($rnum==0){
            $stmt->close();
            $stmt = $conn->prepare($Connection);
            $stmt->bind_param("ssssii", $username, $password, $email, $gender);
            $stmt->execute();
            echo "New User Has Been Registered Sucessfully";

        
    } else {
        echo " This Email Has Been Already Registered"

    }
    $stmt->close();
    $conn->close();
}else{
    echo "All field Are requierd";
    die();
}

}
