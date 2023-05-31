## EC2 script         

### Tips:
install certifi     
        
    pip install certifi     #for retrieving your ip with certification(avoid error)

### Allows creating:

VPC,    
Internet gateway for VPC,   
Desired amount of private and public subnets.

    
### Launch vpc with:
#### Created security group with:    
ssh access only from host machine(on which this script will run)
gives access to http requests from any ip   

creates and downloads .pem key

### command examples:    
To create vpc:

    python main.py -vpc True -igw True -pub 3 -priv 3
to launch ec2 instance:
    
    python main.py -vid vpc-038a43744418c24d7 -sid subnet-0321f7038406c24cd

### arguments:
        
        -vpc True //to create vpc (takes only True or False arguments)

        -igw True //for script to create internet gateway and atttach it to vpc (takes only True or False arguments)

        -pub/--public_subnets X(number of subnets) //to pass amount of public subnets to create with vpc

        -priv/--private_subnets X(number of subnets) //to pass amount of private subnets to create with vpc

        -vid/--vpc_id //pass vpc id to which you want operation on e.g. launch instance

        -sid/--subnet_id //pass subnet id to which we want operation on e.g launch instance

there's time.sleep() function used to slow down creating subnets. Otherways it gives errors

# RDS
## launching RDS

command example:    

    python main.py -vid vpc-081b5d31efb75b7f7 --rds_type mysql -rds_i mysql1818-btu -sid subnet-067ffb82773cac341 subnet-01e3488b70076ea46


### Arguments for launching RDS:
    
    -rds_i/--rds_identifier //takes unique name for RDS database

    -rds/--rds_type //to pass what type of rds do you want made. takes only["mysql", "postgres", "mariadb", "aurora-mysql"]. currently working only for mysql
    
    -vid/--vpc_id //pass vpc id to which we create RDS on

    -sid/--subnet_id //subnets to where RDS database will be setup. requires passing of at least 2 different AZ subnets

## Getting RDS details

command example:

    python main.py -rds_dets True -rds_i mysql1818-btu

### Arguments for getting RDS details:

    -rds_dets/--rds_details //takes only ["True","False"] arguments. if true, returns details
    -rds_i/--rds_identifier //takes database's unique identifier to return details of
    