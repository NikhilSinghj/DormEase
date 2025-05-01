import pandas as pd

# Create a DataFrame with the dummy data
data = {
    'std_name': ['John Doe', 'Jane Smith', 'Alice Jones'],
    'dept': ['CSE', 'ECE', 'ME'],
    'year': ['2', '3', '1'],
    'u_rollno': ['123456', '123457', '123458'],
    'std_contact': ['9876543210', '9876543213', '9876543216'],
    'f_contact': ['9876543211', '9876543214', '9876543217'],
    'm_contact': ['9876543212', '9876543215', '9876543218'],
    'room_altd': ['A101', 'B202', 'C303'],
    'seater_altd': ['2', '3', '1']
}

df = pd.DataFrame(data)

# Save the DataFrame as an .xls file
df.to_excel('students_data.xls', index=False, engine='xlwt')
