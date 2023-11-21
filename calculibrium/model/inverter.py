from calculibrium.models import DBInverter
from django.forms.models import model_to_dict
from django.core.serializers import serialize

def find_combinations(array, target_sum, tolerance):
    result = []
    def is_within_tolerance(val):
        lower_bound = target_sum / (1.3 + tolerance)
        upper_bound = target_sum / (1.3 - tolerance)
        return target_sum-lower_bound >= val >= target_sum-upper_bound

    def backtrack(start, target, current_combination):
        if is_within_tolerance(target):
            result.append(current_combination[:])
            return

        for i in range(start, len(array)):
            if float(array[i].ca_power) <= target:
                current_combination.append(array[i])
                backtrack(i, target - float(array[i].ca_power), current_combination)
                current_combination.pop()

    backtrack(0, target_sum, [])
    return result
    
def lookfor(power_kwp):
    brands = list(DBInverter.objects.values_list('brand', flat=True).distinct())

    choices = []
    for brand in brands:
        inverters = DBInverter.objects.filter(brand=brand)
        if power_kwp < 300:
            potencias = [obj for obj in inverters if obj.ca_power > 0.2 * power_kwp]
        else:
            potencias = [obj for obj in inverters if obj.ca_power >= 100]
        combinations = find_combinations(potencias, power_kwp, 0.12)
        # Get inverters based on combinations
        for combination in combinations:
            inverter_objects = []
            for i in combination:
                obj = model_to_dict(i)
                inverter_objects.append({'pk': obj['inverter_id'], 'model': obj['model'], 'price': float(obj['price'])})
            choices.append(inverter_objects)
    return choices

def get_cheaper(power_kwp):
    combinations = lookfor(power_kwp)
    min = combinations[0]
    for combination in combinations:
        if sum([inverter['price'] for inverter in min]) > sum([inverter['price'] for inverter in combination]):
            min = combination
    return min