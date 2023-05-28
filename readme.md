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
        
        -vpc True #to create vpc (takes only True or False arguments)

        -igw True #for script to create internet gateway and atttach it to vpc (takes only True or False arguments)

        -pub/--public_subnets X(number of subnets) #to pass amount of public subnets to create with vpc

        -priv/--private_subnets X(number of subnets) #to pass amount of private subnets to create with vpc

        -vid/--vpc_id #pass vpc id to which you want operation on e.g. launch instance

        -sid/--subnet_id #pass subnet id to which we want operation on e.g launch instance

there's time.sleep() function used to slow down creating subnets. Otherways it gives errors


