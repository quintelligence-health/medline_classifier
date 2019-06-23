import plotly.plotly as py
import plotly.graph_objs as go

import json

py.sign_in('lstopar', 'PcUGyNuqKeHZhyUX58c4')

from sets import Set

def plot(results, key, suffix):
    print 'generating chart `' + key + '-' + suffix + '`'

    data_x = []
    data_y = []

    for valN in range(len(results)):
        result_tup = results[valN]
        cutoff = result_tup[0]
        val = result_tup[1]
        data_x.append(cutoff)
        data_y.append(val[key])

    trace = go.Scatter(x = data_x, y = data_y)
    data = [trace]
    py.plot(data, filename=key + '-' + suffix)

# for key in result_map.keys():
#     results = result_map[key]

#     results.sort()

#     plot(results, 'precision', key)
#     plot(results, 'recall', key)
#     plot(results, 'f1_global', key)
#     plot(results, 'f1_dataset', key)

dataset = 'major'
fname = 'data/eval1-' + dataset + '.json'
with open(fname, 'r') as f:
    results = json.load(f)

    results.sort(lambda val1, val2: int(10000*(val1[0] - val2[0])))

    plot(results, 'f05_median', dataset)
    plot(results, 'f05_dataset', dataset)
    plot(results, 'precision_median', dataset)
    plot(results, 'precision_mean', dataset)
    plot(results, 'recall_median', dataset)
    plot(results, 'recall_mean', dataset)
    plot(results, 'f1_dataset', dataset)
    plot(results, 'f1_median', dataset)
# results_all = [(0.15, {'fp': 21959075, 'avgHeadings': 12.029616899267653, 'fn': 5229836, 'f1_global': 0.1131710207125426, 'recall': 0.2490903010869005, 'avgClassifiedHeadings': 40.92494472847865, 'f1_dataset': 0.13015330787178003, 'precision': 0.07321844697113258, 'tp': 1734831}), (0.16, {'fp': 18788157, 'avgHeadings': 12.029616899267653, 'fn': 5351680, 'f1_global': 0.11788336914261376, 'recall': 0.23159571017537522, 'avgClassifiedHeadings': 35.237570816636726, 'f1_dataset': 0.1337480411686993, 'precision': 0.07906355643585478, 'tp': 1612987}), (0.17, {'fp': 16014971, 'avgHeadings': 12.029616899267653, 'fn': 5470417, 'f1_global': 0.12210973589484433, 'recall': 0.21454722817329241, 'avgClassifiedHeadings': 30.24254007185298, 'f1_dataset': 0.136057053411706, 'precision': 0.08534074702695225, 'tp': 1494250}), (0.18, {'fp': 13624387, 'avgHeadings': 12.029616899267653, 'fn': 5582943, 'f1_global': 0.12577834066686214, 'recall': 0.19839053324444658, 'avgClassifiedHeadings': 25.91908076551057, 'f1_dataset': 0.13722429102765277, 'precision': 0.09207742099202118, 'tp': 1381724}), (0.19, {'fp': 11573360, 'avgHeadings': 12.029616899267653, 'fn': 5689554, 'f1_global': 0.1287138737221864, 'recall': 0.18308312515156863, 'avgClassifiedHeadings': 22.192332803647922, 'f1_dataset': 0.13734080384999883, 'precision': 0.09924237689568247, 'tp': 1275113}), (0.2, {'fp': 9826379, 'avgHeadings': 12.029616899267653, 'fn': 5789322, 'f1_global': 0.1308381855877455, 'recall': 0.16875824788177238, 'avgClassifiedHeadings': 19.002563216802542, 'f1_dataset': 0.1364343827568809, 'precision': 0.10683280184087512, 'tp': 1175345}), (0.21, {'fp': 8343465, 'avgHeadings': 12.029616899267653, 'fn': 5883067, 'f1_global': 0.13198507455765598, 'recall': 0.15529816429127194, 'avgClassifiedHeadings': 16.279302542489983, 'f1_dataset': 0.1344974808860965, 'precision': 0.11475782925634996, 'tp': 1081600}), (0.22, {'fp': 7090669, 'avgHeadings': 12.029616899267653, 'fn': 5970118, 'f1_global': 0.1321669899803221, 'recall': 0.142799217823336, 'avgClassifiedHeadings': 13.965071852977752, 'f1_dataset': 0.1318047524004906, 'precision': 0.12300830973265038, 'tp': 994549}), (0.23, {'fp': 6030713, 'avgHeadings': 12.029616899267653, 'fn': 6050372, 'f1_global': 0.13146173436834432, 'recall': 0.13127619741187913, 'avgClassifiedHeadings': 11.995661185574132, 'f1_dataset': 0.12855258293789387, 'precision': 0.13164779651801697, 'tp': 914295}), (0.24, {'fp': 5136981, 'avgHeadings': 12.029616899267653, 'fn': 6124947, 'f1_global': 0.12977298845068003, 'recall': 0.12056857851208105, 'avgClassifiedHeadings': 10.323167403620285, 'f1_dataset': 0.1246610227620108, 'precision': 0.14049891403300918, 'tp': 839720}), (0.25, {'fp': 4382783, 'avgHeadings': 12.029616899267653, 'fn': 6193670, 'f1_global': 0.12724353211265438, 'recall': 0.11070120078964292, 'avgClassifiedHeadings': 8.901789415503663, 'f1_dataset': 0.12032592964287106, 'precision': 0.14959835305348695, 'tp': 770997}), (0.26, {'fp': 3745267, 'avgHeadings': 12.029616899267653, 'fn': 6256853, 'f1_global': 0.12398486987101137, 'recall': 0.10162926669717304, 'avgClassifiedHeadings': 7.6915175487080285, 'f1_dataset': 0.11570884570406298, 'precision': 0.1589492757935461, 'tp': 707814}), (0.27, {'fp': 3206657, 'avgHeadings': 12.029616899267653, 'fn': 6315299, 'f1_global': 0.12002337743279266, 'recall': 0.09323747998289078, 'avgClassifiedHeadings': 6.660261503385381, 'f1_dataset': 0.1107726773250794, 'precision': 0.16840347248785992, 'tp': 649368}), (0.28, {'fp': 2751672, 'avgHeadings': 12.029616899267653, 'fn': 6368618, 'f1_global': 0.11559863728944254, 'recall': 0.08558183758103582, 'avgClassifiedHeadings': 5.782301022523145, 'f1_dataset': 0.1057585143163383, 'precision': 0.17804619919043432, 'tp': 596049}), (0.29, {'fp': 2365919, 'avgHeadings': 12.029616899267653, 'fn': 6417817, 'f1_global': 0.11072711582236523, 'recall': 0.07851775253576374, 'avgClassifiedHeadings': 5.031036686472295, 'f1_dataset': 0.10060917265743526, 'precision': 0.18774231667530106, 'tp': 546850}), (0.3, {'fp': 2038735, 'avgHeadings': 12.029616899267653, 'fn': 6463356, 'f1_global': 0.10548682532549904, 'recall': 0.07197917718104828, 'avgClassifiedHeadings': 4.387256459859057, 'f1_dataset': 0.09534562231488337, 'precision': 0.19736296114322338, 'tp': 501311}), (0.31, {'fp': 1760406, 'avgHeadings': 12.029616899267653, 'fn': 6505720, 'f1_global': 0.09994468653160599, 'recall': 0.06589647430379658, 'avgClassifiedHeadings': 3.8333442724886004, 'f1_dataset': 0.08997150531859939, 'precision': 0.2067931509768838, 'tp': 458947}), (0.32, {'fp': 1524125, 'avgHeadings': 12.029616899267653, 'fn': 6544182, 'f1_global': 0.0943926201868008, 'recall': 0.06037402793270662, 'avgClassifiedHeadings': 3.3587985353046843, 'f1_dataset': 0.08474998091109406, 'precision': 0.21623101804474934, 'tp': 420485}), (0.33, {'fp': 1322260, 'avgHeadings': 12.029616899267653, 'fn': 6579475, 'f1_global': 0.08883457434105783, 'recall': 0.05530659254778441, 'avgClassifiedHeadings': 2.949170927179771, 'f1_dataset': 0.0796625584548051, 'precision': 0.2255946287216273, 'tp': 385192}), (0.34, {'fp': 1148332, 'avgHeadings': 12.029616899267653, 'fn': 6611626, 'f1_global': 0.08340168484911481, 'recall': 0.050690291438197976, 'avgClassifiedHeadings': 2.593224056929667, 'f1_dataset': 0.07479269001475491, 'precision': 0.23514543021620876, 'tp': 353041}), (0.35000000000000003, {'fp': 999414, 'avgHeadings': 12.029616899267653, 'fn': 6641497, 'f1_global': 0.07799208688140374, 'recall': 0.046401357021089454, 'avgClassifiedHeadings': 2.2844134309796877, 'f1_dataset': 0.0700147887603538, 'precision': 0.2443474289723753, 'tp': 323170}), (0.36, {'fp': 869669, 'avgHeadings': 12.029616899267653, 'fn': 6669114, 'f1_global': 0.07270775775659422, 'recall': 0.04243605616750951, 'avgClassifiedHeadings': 2.0126122702777396, 'f1_dataset': 0.065349725035774, 'precision': 0.25364522811962015, 'tp': 295553}), (0.37, {'fp': 757643, 'avgHeadings': 12.029616899267653, 'fn': 6694324, 'f1_global': 0.06764787611823007, 'recall': 0.038816356905506035, 'avgClassifiedHeadings': 1.775573442033992, 'f1_dataset': 0.06093877319369776, 'precision': 0.2629831534670706, 'tp': 270343}), (0.38, {'fp': 660825, 'avgHeadings': 12.029616899267653, 'fn': 6717483, 'f1_global': 0.06279542051520981, 'recall': 0.03549114408485, 'avgClassifiedHeadings': 1.5683449633826172, 'f1_dataset': 0.05670481585839805, 'precision': 0.2722263766108045, 'tp': 247184}), (0.39, {'fp': 575853, 'avgHeadings': 12.029616899267653, 'fn': 6738810, 'f1_global': 0.058162770105030945, 'recall': 0.03242897327323761, 'avgClassifiedHeadings': 1.384741605637695, 'f1_dataset': 0.052663466892456545, 'precision': 0.2817190754761697, 'tp': 225857}), (0.4, {'fp': 502449, 'avgHeadings': 12.029616899267653, 'fn': 6758759, 'f1_global': 0.05367062581845176, 'recall': 0.02956465829593863, 'avgClassifiedHeadings': 1.2234990327483763, 'f1_dataset': 0.04876271904230609, 'precision': 0.29068393479559035, 'tp': 205908}), (0.41000000000000003, {'fp': 438403, 'avgHeadings': 12.029616899267653, 'fn': 6776816, 'f1_global': 0.04949359899806624, 'recall': 0.026972000240643234, 'avgClassifiedHeadings': 1.0816878540831836, 'f1_dataset': 0.045135304875497086, 'precision': 0.2999597607360592, 'tp': 187851}), (0.42, {'fp': 382701, 'avgHeadings': 12.029616899267653, 'fn': 6793687, 'f1_global': 0.0454833960864807, 'recall': 0.024549630298189417, 'avgClassifiedHeadings': 0.9563372253696283, 'f1_dataset': 0.04163314711831906, 'precision': 0.3088059731144829, 'tp': 170980}), (0.43, {'fp': 334008, 'avgHeadings': 12.029616899267653, 'fn': 6809194, 'f1_global': 0.04171449238732582, 'recall': 0.02232310604369168, 'avgClassifiedHeadings': 0.8454487356639492, 'f1_dataset': 0.03834050849001044, 'precision': 0.31762826340552547, 'tp': 155473}), (0.44, {'fp': 290951, 'avgHeadings': 12.029616899267653, 'fn': 6823601, 'f1_global': 0.03814303815060911, 'recall': 0.020254521860126263, 'avgClassifiedHeadings': 0.7461949012021556, 'f1_dataset': 0.0351950376053044, 'precision': 0.3265288171530287, 'tp': 141066}), (0.45, {'fp': 253213, 'avgHeadings': 12.029616899267653, 'fn': 6836894, 'f1_global': 0.03478873831911199, 'recall': 0.01834588789385049, 'avgClassifiedHeadings': 0.6580523697664779, 'f1_dataset': 0.03222765118361944, 'precision': 0.33537452819788655, 'tp': 127773}), (0.46, {'fp': 220680, 'avgHeadings': 12.029616899267653, 'fn': 6849089, 'f1_global': 0.03166119361587744, 'recall': 0.016594906834741702, 'avgClassifiedHeadings': 0.580796600801437, 'f1_dataset': 0.029461706287623988, 'precision': 0.34371821636957334, 'tp': 115578}), (0.47000000000000003, {'fp':191745, 'avgHeadings': 12.029616899267653, 'fn': 6860022, 'f1_global': 0.028823627193671666, 'recall': 0.015025126111557093, 'avgClassifiedHeadings': 0.5119351941412187, 'f1_dataset': 0.026941624831669585, 'precision': 0.35306521812476804, 'tp': 104645}), (0.48, {'fp': 166554, 'avgHeadings': 12.029616899267653, 'fn': 6870206, 'f1_global': 0.02614590567367897, 'recall': 0.013562888218489125, 'avgClassifiedHeadings': 0.4508342545253558, 'f1_dataset': 0.024529047094843187, 'precision': 0.3618987414516407, 'tp': 94461}), (0.49, {'fp': 144326, 'avgHeadings': 12.029616899267653, 'fn': 6879554, 'f1_global': 0.023661869869584906, 'recall': 0.012220684779329723, 'avgClassifiedHeadings': 0.39629508083459997, 'f1_dataset': 0.02232255108402214, 'precision': 0.3709613448454709, 'tp': 85113}), (0.5, {'fp': 124899, 'avgHeadings': 12.029616899267653, 'fn': 6888032, 'f1_global': 0.021387901344101283, 'recall': 0.011003397578089519, 'avgClassifiedHeadings': 0.3480965869835567, 'f1_dataset': 0.020280894791493063, 'precision': 0.3802584179344428, 'tp': 76635})]
# results_major = [(0.15, {'fp': 14467921, 'avgHeadings': 1.8234941315420388, 'fn': 256868, 'f1_global': 0.04364558822679349, 'recall': 0.5667373399519962, 'avgClassifiedHeadings': 45.532596392805296, 'f1_dataset': 0.0689092551039518, 'precision': 0.022696755630028313, 'tp': 336001}), (0.16, {'fp': 12606367, 'avgHeadings': 1.8234941315420388, 'fn': 273467, 'f1_global': 0.04725357687660546, 'recall': 0.5387395866540501, 'avgClassifiedHeadings': 39.755939199330726, 'f1_dataset': 0.07555611181197076, 'precision': 0.024710483376269528, 'tp': 319402}), (0.17, {'fp': 10932373, 'avgHeadings': 1.8234941315420388, 'fn': 290238, 'f1_global': 0.051172514280462766, 'recall': 0.5104517186764699, 'avgClassifiedHeadings': 34.555633473585786, 'f1_dataset': 0.08202844948916503, 'precision': 0.02693643900794339, 'tp': 302631}), (0.18, {'fp': 9449853, 'avgHeadings': 1.8234941315420388, 'fn': 307145, 'f1_global': 0.0553275875189743, 'recall': 0.48193445769638826, 'avgClassifiedHeadings': 29.943828276863265, 'f1_dataset': 0.08788629478737328, 'precision': 0.02934844026193825, 'tp': 285724}), (0.19, {'fp': 8151678, 'avgHeadings': 1.8234941315420388, 'fn': 323902, 'f1_global': 0.05968083036205414, 'recall': 0.4536702037043596, 'avgClassifiedHeadings': 25.89947651386531, 'f1_dataset': 0.09328400489129295, 'precision': 0.03194137741230037, 'tp': 268967}), (0.2, {'fp': 7021313, 'avgHeadings': 1.8234941315420388, 'fn': 340372, 'f1_global': 0.06419405189915592, 'recall': 0.42589003641613915, 'avgClassifiedHeadings': 22.372142663812408, 'f1_dataset': 0.09799659584965603, 'precision': 0.03471316957687924, 'tp': 252497}), (0.21, {'fp': 6043666, 'avgHeadings': 1.8234941315420388, 'fn': 356277, 'f1_global': 0.0688455196593923, 'recall': 0.39906286211625164, 'avgClassifiedHeadings': 19.31626313328904, 'f1_dataset': 0.10224708810708598, 'precision': 0.03767233766510866, 'tp': 236592}), (0.22, {'fp': 5204198, 'avgHeadings': 1.8234941315420388, 'fn': 371725, 'f1_global': 0.07349160738963789, 'recall': 0.373006515773299, 'avgClassifiedHeadings': 16.68678797273689, 'f1_dataset': 0.10564634272309611, 'precision': 0.040761301315198194, 'tp': 221144}), (0.23, {'fp': 4482484, 'avgHeadings': 1.8234941315420388, 'fn': 386371, 'f1_global': 0.07819152793215862, 'recall': 0.3483029134598031, 'avgClassifiedHeadings': 14.421956890824537, 'f1_dataset': 0.10833797719464948, 'precision': 0.044038983301706, 'tp': 206498}), (0.24, {'fp': 3864010, 'avgHeadings': 1.8234941315420388, 'fn': 400538, 'f1_global': 0.08273706715764613, 'recall': 0.32440724679482313, 'avgClassifiedHeadings': 12.47613555276691, 'f1_dataset': 0.11020035554001636, 'precision': 0.04741489928977864, 'tp': 192331}), (0.25, {'fp': 3335342, 'avgHeadings': 1.8234941315420388, 'fn': 413977, 'f1_global': 0.08711347146638397, 'recall': 0.3017395073785271, 'avgClassifiedHeadings': 10.808770699539874, 'f1_dataset': 0.11105874632083462, 'precision': 0.05090497673177142, 'tp': 178892}), (0.26, {'fp': 2882019, 'avgHeadings': 1.8234941315420388, 'fn': 426513, 'f1_global': 0.09137316807113174, 'recall': 0.28059487003031025, 'avgClassifiedHeadings': 9.375922713515907, 'f1_dataset': 0.11140786602684338, 'precision': 0.054572026079468566, 'tp': 166356}), (0.27, {'fp': 2492716, 'avgHeadings': 1.8234941315420388, 'fn': 438425, 'f1_global': 0.09533494916249206, 'recall': 0.26050274175239385, 'avgClassifiedHeadings': 8.141901035899707, 'f1_dataset': 0.11104481518104102, 'precision': 0.05834328110125569, 'tp': 154444}), (0.28, {'fp': 2161146, 'avgHeadings': 1.8234941315420388, 'fn': 449602, 'f1_global': 0.09889751843279322, 'recall': 0.24165034771593724, 'avgClassifiedHeadings': 7.087710071110455, 'f1_dataset': 0.11009923368876755, 'precision': 0.06217071332265527, 'tp': 143267}), (0.29, {'fp': 1876586, 'avgHeadings': 1.8234941315420388, 'fn': 460085, 'f1_global': 0.10205365456439626, 'recall': 0.22396853267753922, 'avgClassifiedHeadings': 6.180242858197387, 'f1_dataset': 0.10867752703133739, 'precision': 0.06608240393755256, 'tp': 132784}), (0.3, {'fp': 1632829, 'avgHeadings': 1.8234941315420388, 'fn': 469939, 'f1_global': 0.10468239329514932, 'recall': 0.20734766027571014, 'avgClassifiedHeadings': 5.400208533254595, 'f1_dataset': 0.10676390549109323, 'precision': 0.07001530392269098, 'tp': 122930}), (0.31, {'fp': 1423295, 'avgHeadings': 1.8234941315420388, 'fn': 479138, 'f1_global': 0.10679493590059604, 'recall': 0.19183158505504588, 'avgClassifiedHeadings': 4.727448881671219, 'f1_dataset': 0.10429822390627108, 'precision': 0.07399419398240498, 'tp': 113731}), (0.32, {'fp': 1243196, 'avgHeadings': 1.8234941315420388, 'fn': 487608, 'f1_global': 0.1084423739238026, 'recall': 0.17754512379631926, 'avgClassifiedHeadings': 4.14746499840063, 'f1_dataset': 0.10165794578122726, 'precision': 0.07806033117852479, 'tp': 105261}), (0.33, {'fp': 1088253, 'avgHeadings': 1.8234941315420388, 'fn': 495531, 'f1_global': 0.10946324348031443, 'recall': 0.16418129468735926, 'avgClassifiedHeadings': 3.646536133461283, 'f1_dataset': 0.09857478825150588, 'precision': 0.08210082566416244, 'tp': 97338}), (0.34, {'fp': 954081, 'avgHeadings': 1.8234941315420388, 'fn': 502823, 'f1_global': 0.110013708035939, 'recall': 0.15188178164147562, 'avgClassifiedHeadings': 3.2114336507467827, 'f1_dataset': 0.09533475988251523, 'precision': 0.08624046691638086, 'tp': 90046}), (0.35000000000000003, {'fp': 837318, 'avgHeadings': 1.8234941315420388, 'fn': 509777, 'f1_global': 0.109817158633669, 'recall': 0.14015237767533806, 'avgClassifiedHeadings': 2.8309158239216554, 'f1_dataset': 0.09162999059685271, 'precision': 0.09027715909214372, 'tp': 83092}), (0.36, {'fp': 735910, 'avgHeadings': 1.8234941315420388, 'fn': 516402, 'f1_global': 0.10883076699737983, 'recall': 0.12897790236966344, 'avgClassifiedHeadings': 2.4986374597081764, 'f1_dataset': 0.08766402579833271, 'precision': 0.09412748022162125, 'tp': 76467}), (0.37, {'fp': 647422, 'avgHeadings': 1.8234941315420388, 'fn': 522357, 'f1_global': 0.10758596066685841, 'recall': 0.11893352494395895, 'avgClassifiedHeadings': 2.208158017765311, 'f1_dataset': 0.08377400992851308, 'precision': 0.09821515626784635, 'tp': 70512}), (0.38, {'fp': 569535, 'avgHeadings': 1.8234941315420388, 'fn': 527860, 'f1_global': 0.10592848535904377, 'recall': 0.10965154190892086, 'avgClassifiedHeadings': 1.9516744174602003, 'f1_dataset': 0.07988933477404105, 'precision': 0.1024499483093371, 'tp': 65009}), (0.39, {'fp': 501226, 'avgHeadings': 1.8234941315420388, 'fn': 533042, 'f1_global': 0.10369331722594768, 'recall': 0.10091099382831621, 'avgClassifiedHeadings': 1.7256372874683201, 'f1_dataset': 0.07575035614429655, 'precision': 0.10663341965910529, 'tp': 59827}), (0.4, {'fp': 441593, 'avgHeadings': 1.8234941315420388, 'fn': 537899, 'f1_global': 0.10091497220569985, 'recall': 0.09271862755515974, 'avgClassifiedHeadings': 1.527284638665387, 'f1_dataset': 0.0717158736695446, 'precision': 0.11070095838795883, 'tp': 54970}), (0.41000000000000003, {'fp': 389211, 'avgHeadings': 1.8234941315420388, 'fn': 542361, 'f1_global': 0.09782798173133914, 'recall': 0.08519251301720954, 'avgClassifiedHeadings': 1.3524488816712188, 'f1_dataset': 0.06764478951412112, 'precision': 0.11486426558779585, 'tp': 50508}), (0.42, {'fp': 342841, 'avgHeadings': 1.8234941315420388, 'fn': 546574, 'f1_global': 0.09428668896797879, 'recall': 0.07808639007942733, 'avgClassifiedHeadings': 1.1968701557540415, 'f1_dataset': 0.0636022276280099, 'precision': 0.11896868960980223, 'tp': 46295}), (0.43, {'fp': 301901, 'avgHeadings': 1.8234941315420388, 'fn': 550576, 'f1_global': 0.09026714319101276, 'recall': 0.07133616363817302, 'avgClassifiedHeadings': 1.0586415196476464, 'f1_dataset': 0.059503300876269136, 'precision': 0.12287547139113407, 'tp': 42293}), (0.44, {'fp': 265613, 'avgHeadings': 1.8234941315420388, 'fn': 554128, 'f1_global': 0.08635757219777022, 'recall': 0.06534495816107774, 'avgClassifiedHeadings': 0.9361051647351197, 'f1_dataset': 0.05558036634789335, 'precision': 0.1272892749889931, 'tp': 38741}), (0.45, {'fp': 233543, 'avgHeadings': 1.8234941315420388, 'fn': 557519, 'f1_global': 0.08204121323520881, 'recall': 0.05962531351782603, 'avgClassifiedHeadings': 0.827037351443124, 'f1_dataset': 0.05170301716679731, 'precision': 0.13146493214773164, 'tp': 35350}), (0.46, {'fp': 205286, 'avgHeadings': 1.8234941315420388, 'fn': 560702, 'f1_global': 0.07748078456309722, 'recall': 0.05425650523134116, 'avgClassifiedHeadings': 0.7303369749760095, 'f1_dataset': 0.04799010965523122, 'precision': 0.13546680816835333, 'tp': 32167}), (0.47000000000000003, {'fp': 180261, 'avgHeadings': 1.8234941315420388, 'fn': 563570, 'f1_global': 0.073025775489171, 'recall': 0.049419011619767604, 'avgClassifiedHeadings': 0.6445461479786423, 'f1_dataset': 0.044483837464826294, 'precision': 0.13981198702042374, 'tp': 29299}), (0.48, {'fp': 158225, 'avgHeadings': 1.8234941315420388, 'fn': 566246, 'f1_global': 0.06846449286822842, 'recall': 0.044905366952901905, 'avgClassifiedHeadings': 0.5685391599616151, 'f1_dataset': 0.04108970920507567, 'precision': 0.14402644334804812, 'tp': 26623}), (0.49, {'fp': 138369, 'avgHeadings': 1.8234941315420388, 'fn': 568706, 'f1_global': 0.06397396879273393, 'recall': 0.04075605234883254, 'avgClassifiedHeadings': 0.49990157722496986, 'f1_dataset': 0.037804603392918065, 'precision': 0.14866610882780007, 'tp': 24163}), (0.5, {'fp': 120828, 'avgHeadings': 1.8234941315420388, 'fn': 570916, 'f1_global': 0.05968327329572488, 'recall': 0.03702841605818486, 'avgClassifiedHeadings': 0.4391531950493344, 'f1_dataset': 0.03482034532815653, 'precision': 0.1537529503225219, 'tp': 21953})]

