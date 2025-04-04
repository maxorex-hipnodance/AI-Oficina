from flask import Flask, request, jsonify, render_template
from car import Car
from persistencia import save_car, load_cars

app = Flask(__name__, template_folder='template')
CAR_FILE = 'carros.txt'


@app.route('/')
def index():
    cars = load_cars(CAR_FILE)
    return render_template('carros.html', cars=cars)


@app.route('/add_car', methods=['POST'])
def add_car():
    try:
        data = request.get_json()
        new_car = Car(
            data['make'],
            data['model'],
            int(data['year']),
            data['plate'],
            data['complaint'],
            data['car_status']
        )

        cars = load_cars(CAR_FILE)
        cars.append(new_car)
        save_car(CAR_FILE, cars)
        return jsonify({'success': True}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/delete_car', methods=['POST'])
def delete_car():
    try:
        plate = request.json['plate']
        cars = load_cars(CAR_FILE)
        updated_cars = [car for car in cars if car.plate != plate]

        if len(updated_cars) == len(cars):
            return jsonify({'success': False, 'error': 'Car not found'}), 404

        save_car(CAR_FILE, updated_cars)
        return jsonify({'success': True}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/update_car', methods=['POST'])
def update_car():
    try:
        data = request.get_json()
        plate = data['plate']
        updated_data = {
            'make': data['make'],
            'model': data['model'],
            'year': int(data['year']),
            'complaint': data['complaint'],
            'car_status': data['car_status']
        }

        cars = load_cars(CAR_FILE)
        updated = False

        for car in cars:
            if car.plate == plate:
                car.make = updated_data['make']
                car.model = updated_data['model']
                car.year = updated_data['year']
                car.complaint = updated_data['complaint']
                car.car_status = updated_data['car_status']
                updated = True
                break

        if not updated:
            return jsonify({'success': False, 'error': 'Car not found'}), 404

        save_car(CAR_FILE, cars)
        return jsonify({'success': True}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
