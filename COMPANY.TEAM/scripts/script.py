import json
from kestra import Kestra

# Initialize a dictionary to accumulate service-wise costs
service_costs = {}
total_cost = 0

try:
    # Load the JSON data from the file
    with open('COMPANY.TEAM/scripts/output.json', 'r') as file:
        data = json.load(file)

    # Check if data was loaded properly
    if not data:
        raise ValueError("The JSON file is empty or doesn't contain valid data.")
    else:
        # Extract the 'ResultsByTime' field
        results = data.get('ResultsByTime', [])

        # Check if 'ResultsByTime' contains data
        if not results:
            raise ValueError("No cost data found in the 'ResultsByTime' field.")
        else:
            # Loop through results to calculate costs
            for result in results:
                for group in result.get('Groups', []):
                    service_name = group['Keys'][0]
                    cost = group['Metrics'].get('BlendedCost', {})
                    amount = float(cost.get('Amount', '0'))

                    # Accumulate costs by service
                    if service_name not in service_costs:
                        service_costs[service_name] = 0
                    service_costs[service_name] += amount

                    # Add to the total cost
                    total_cost += amount

            # Prepare service costs in a readable format for Discord
            service_costs_str = "\n".join([f"- {service}: ${round(cost, 2)}" for service, cost in service_costs.items()])

            # Prepare the outputs for Kestra
            Kestra.outputs({
                'total_cost': round(total_cost, 2),
                'service_costs': service_costs_str
            })

except json.JSONDecodeError:
    raise ValueError("The JSON file is invalid.")
except FileNotFoundError:
    raise ValueError("The file 'output.json' was not found.")
except Exception as e:
    raise RuntimeError(f"Unexpected error: {e}")
