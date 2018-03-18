"""
if all bigger than max value, out by get_position
if all smaller than min value, in
if any one bigger than max value, stop in
if all smaller than max value, start in
"""

# variable
_max_180 = 0.1
_max_90 = _max_180 / 2.0
_max_30 = _max_180 / 6.0

_min_180 = 0.06
_min_90 = _min_180 / 2.0
_min_30 = _min_180 / 6.0

_max_180_position = 0.5
_in_flow_rate_30 = 1.5
_in_flow_rate_90 = 1.2
_in_flow_rate_180 = 1

config_str = """
if all bigger than max value, out by get_position (_max_180 / cur_180_rate * _max_180_position)
if all smaller than min value, in
if any one bigger than max value * _in_flow_rate, stop
if all smaller than max value, continue
# variable(percent)
_max_180 = %s
_max_90 = %s
_max_30 = %s
_min_180 = %s
_min_90 = %s
_min_30 = %s
_max_180_position = %s
# float
_in_flow_rate = %s, %s, %s
"""
fund_config_str = config_str % (_max_180 * 100, _max_90 * 100, _max_30 * 100,
                                _min_180 * 100, _min_90 * 100, _min_30 * 100, _max_180_position * 100,
                                _in_flow_rate_30, _in_flow_rate_90, _in_flow_rate_180)


# rule function
def _get_position(cur_180_rate):
    return _max_180 / cur_180_rate * _max_180_position


def fund_strategy(cur_30_rate, cur_90_rate, cur_180_rate):
    if cur_30_rate >= _max_30 and cur_90_rate >= _max_90 and cur_180_rate >= _max_180:
        return "out at %s" % _get_position(cur_180_rate)

    if cur_30_rate < _min_30 and cur_90_rate < _min_90 and cur_180_rate < _min_180:
        return "in"

    if cur_180_rate >= _max_180 * _in_flow_rate_180:
        return "stop and out 50%"
    elif cur_30_rate >= _max_30 * _in_flow_rate_30 or cur_90_rate >= _max_90 * _in_flow_rate_90:
        return "stop in"
    else:
        return "continue"