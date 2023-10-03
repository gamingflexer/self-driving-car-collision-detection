from flask import Flask, request, jsonify
import pymysql

app = Flask(__name__)

# Database credentials
db_host = '127.0.0.1'
db_user = 'root'
db_pass = ''
db_name = 'bms_db'
db_port = 3306

# Initialize the databaseaconnection
conn = pymysql.connect(host=db_host, user=db_user, passwd=db_pass, db=db_name, port=db_port)

@app.route('/')
def index():
    return 'Hello World!'

@app.route('/save_data', methods=['POST'])
def save_data():
    try:
        # Parse the JSON data from the POST request
        data = request.get_json()

        # Define the SQL query to insert data into the table
        insert_query = """
        INSERT INTO bms_data (Time, Time_Since_Power_On, Time_Since_Faults_Occurred, Time_Since_Faults_Cleared, 
        Is_Ready_Power_Status, Is_Charging_Power_Status, Always_On_Power_Status, Discharge_Enable_Output_Active, 
        Pack_Amperage, Pack_Voltage, Pack_State_of_Charge, Pack_Amp_hours, CANBUS_1_Errors_Present, 
        Highest_battery_temperature, Lowest_battery_temperature, Average_battery_temperature, Main_Temperature_Sensor_1, 
        Main_Temperature_Sensor_2, Main_Temperature_Sensor_3, Main_Temperature_Sensor_4, Main_Temperature_Sensor_5, 
        Main_Temperature_Sensor_6, Main_Temperature_Sensor_7, Main_Temperature_Sensor_8, Lowest_Cell_Voltage, 
        Highest_Cell_Voltage)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        # Get a cursor from the database connection
        cursor = conn.cursor()

        # Execute the SQL query with data from the request
        cursor.execute(insert_query, (
            data['Time'], data['Time_Since_Power_On'], data['Time_Since_Faults_Occurred'],
            data['Time_Since_Faults_Cleared'], data['Is_Ready_Power_Status'], data['Is_Charging_Power_Status'],
            data['Always_On_Power_Status'], data['Discharge_Enable_Output_Active'], data['Pack_Amperage'],
            data['Pack_Voltage'], data['Pack_State_of_Charge'], data['Pack_Amp_hours'],
            data['CANBUS_1_Errors_Present'], data['Highest_battery_temperature'],
            data['Lowest_battery_temperature'], data['Average_battery_temperature'],
            data['Main_Temperature_Sensor_1'], data['Main_Temperature_Sensor_2'],
            data['Main_Temperature_Sensor_3'], data['Main_Temperature_Sensor_4'],
            data['Main_Temperature_Sensor_5'], data['Main_Temperature_Sensor_6'],
            data['Main_Temperature_Sensor_7'], data['Main_Temperature_Sensor_8'],
            data['Lowest_Cell_Voltage'], data['Highest_Cell_Voltage']
        ))

        # Commit the transaction
        conn.commit()

        # Close the cursor
        cursor.close()

        return jsonify({"message": "Data saved successfully"}), 201
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
