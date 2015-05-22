import os, sys
import subprocess as sp

sys.path.append ( "card_info_2014_eejj_ttbarFromData_signalInject" )
sys.path.append ( "card_info_2014_enujj_MT_signalInject" )

from enujj_jes_card_info      import *
from eejj_jes_card_info       import *
                              
from eejj_ees_card_info       import *
from enujj_ees_card_info      import *

from enujj_jer_card_info      import *
from eejj_jer_card_info       import *
                              
from eejj_eer_card_info       import *
from enujj_eer_card_info      import *
                              
from enujj_shape_card_info    import *
from eejj_shape_card_info     import *
                              
from eejj_ereco_card_info     import *
from enujj_ereco_card_info    import *
                              
from enujj_mcstat_card_info   import *
from eejj_mcstat_card_info    import *

from enujj_entries  import *
from eejj_entries   import *

from enujj_data_card_info     import *
from eejj_data_card_info      import *

from eejj_norm_card_info      import *
from enujj_norm_card_info     import *
                               
from enujj_lumi_card_info     import *
from eejj_lumi_card_info      import * 
           
from enujj_pdf_card_info     import *
from eejj_pdf_card_info      import * 

from eejj_pu_card_info import *
from enujj_pu_card_info import *

signal_names = [ "LQ_BetaHalf_M", "LQ_M" ] 
# signal_names = [ "LQ_BetaHalf_M"]
mass_points = [ "300", "350", "400", "450", "500", "550", "600", "650", "700", "750", "800", "850", "900", "950", "1000", "1050", "1100", "1150", "1200" ]
systematics = [ "jes", "ees", "shape", "norm", "lumi", "eer", "jer", "pu", "ereco", "pdf" ]
background_names =  [ "gjet", "qcd", "ttbar", "wjet", "zjet", "vv","stop"  ]

n_background = len ( background_names  )
n_systematics = len ( systematics ) + n_background + 1
n_channels = 1

d_systematics_enujj = {}
d_systematics_eejj = {}

                        
d_systematics_enujj = { "jes"   : enujj_jes  ,
                       "ees"   : enujj_ees  ,
                       "jer"   : enujj_jer  ,
                       "eer"   : enujj_eer  ,
                       "pu"    : enujj_pu   , 
                       "shape" : enujj_shape,
                       "ereco" : enujj_ereco,
                       "norm"  : enujj_norm ,
                       "lumi"  : enujj_lumi ,
                        "pdf"  : enujj_pdf   }

                        
d_systematics_eejj = { "jes"   : eejj_jes  ,
                       "ees"   : eejj_ees  ,
                       "jer"   : eejj_jer  ,
                       "eer"   : eejj_eer  ,
                       "pu"    : eejj_pu   , 
                       "shape" : eejj_shape,
                       "ereco" : eejj_ereco,
                       "norm"  : eejj_norm ,
                       "lumi"  : eejj_lumi ,
                       "pdf"   : eejj_pdf   }

card_file_path = "tmp_card_file.txt"
card_file = open ( card_file_path, "w" ) 

for i_signal_name, signal_name in enumerate(signal_names):
    
    for i_mass_point, mass_point in enumerate(mass_points):
        
        txt_file_name = signal_name + "_" + mass_point + ".txt\n"

        card_file.write ( txt_file_name + "\n\n" )
        card_file.write ( "imax " + str ( n_channels    ) + "\n" ) 
        card_file.write ( "jmax " + str ( n_background  ) + "\n" ) 
        card_file.write ( "kmax " + str ( n_systematics ) + "\n\n" ) 
        
        card_file.write ( "bin 1\n\n" )

        if "BetaHalf" in signal_name: 
            card_file.write ( "observation " + str ( enujj_data["data"][i_mass_point] ) + "\n\n" )
        else : 
            card_file.write ( "observation " + str ( eejj_data["data"][i_mass_point] ) + "\n\n" )
        
        line = "bin " 
        for i_channel in range (0, n_background + 1) :
            line = line + "1 " 
        card_file.write (line + "\n") 

        line = "process " + signal_name + "_" + mass_point + " "
        for background_name in background_names:
            line = line + background_name + " "
        card_file.write (line + "\n") 

        line = "process 0 "
        for background_name in background_names:
            line = line + "1 "
        card_file.write (line + "\n\n") 

        line = "rate "
        
        total_bkg = 0.0

        if "BetaHalf" in signal_name: 
            total_data = enujj_data["data"][i_mass_point]
            total_signal = enujj_n["LQ"][i_mass_point]
            line = line + str(enujj_n["LQ"][i_mass_point]) + " "
            for background_name in background_names:
                line = line + str(enujj_n[background_name][i_mass_point]) + " "
                total_bkg = total_bkg + float ( enujj_n[background_name][i_mass_point] ) 
        else:
            total_data = eejj_data["data"][i_mass_point]
            total_signal = eejj_n["LQ"][i_mass_point]

            line = line + str(eejj_n["LQ"][i_mass_point]) + " "
            for background_name in background_names:
                line = line + str(eejj_n[background_name][i_mass_point]) + " "
                total_bkg = total_bkg + float ( eejj_n[background_name][i_mass_point] ) 
        card_file.write ( line + "\n\n")

        print signal_name, mass_point, total_signal, total_bkg, total_data

        for systematic in systematics :
            
            line = systematic + " lnN "
            if "BetaHalf" in signal_name: 
                line = line + str(1.0 + d_systematics_enujj[systematic]["LQ"][i_mass_point] / 100.) + " "
                for background_name in background_names:
                    line = line + str(1.0 + d_systematics_enujj[systematic][background_name][i_mass_point] / 100.) + " "
            else:
                line = line + str(1.0 + d_systematics_eejj[systematic]["LQ"][i_mass_point] / 100.) + " "
                for background_name in background_names:
                    line = line + str(1.0 + d_systematics_eejj[systematic][background_name][i_mass_point] / 100.) + " "
                    
            card_file.write ( line + "\n")
        
        card_file.write("\n")

        for i_background_name ,background_name in enumerate(background_names):

            if "BetaHalf" in signal_name: 
                n       = float (enujj_n[background_name][i_mass_point]       )
                e       = float (enujj_e[background_name][i_mass_point]       )
                entries = float (enujj_entries [background_name][i_mass_point])
            else:
                n       = float (eejj_n[background_name][i_mass_point]       )
                e       = float (eejj_e[background_name][i_mass_point]       )
                entries = float (eejj_entries [background_name][i_mass_point])

            if n!= 0.0: 
                ln_f = 1.0 + e / n 
                weight = n / entries
            else: 
                if background_name == "vv":
                    ln_f = "blah"
                    weight = 0.111
                elif background_name == "stop":
                    ln_f = "blah"
                    weight = 0.438
                elif background_name == "wjet":
                    ln_f = "blah"
                    weight = "1.20"
                elif background_name == "zjet":
                    ln_f = "blah"
                    weight = "1.20"
                elif background_name == "ttbar":
                    ln_f = "blah"
                    weight = "0.19"
                else:
                    ln_f = "blah"
                    weight = "blah"
            
            line_ln = "stat_" + background_name + " lnN -"
            line_gm = "stat_" + background_name + " gmN " + str(int(entries)) + " -"
            for i_tmp in range ( 0, i_background_name ):
                line_ln = line_ln + " -"
                line_gm = line_gm + " -"
            line_ln = line_ln + " " + str(ln_f)
            line_gm = line_gm + " " + str(weight)
            for i_tmp in range ( i_background_name, len(background_names) -1 ):
                line_ln = line_ln + " -"
                line_gm = line_gm + " -"

            if entries > 10:
                card_file.write (line_ln + "\n")
            else:
                card_file.write (line_gm + "\n")
            
        if "BetaHalf" in signal_name: 
            n       = enujj_n["LQ"][i_mass_point]
            e       = enujj_e["LQ"][i_mass_point]
            entries = enujj_entries ["LQ"][i_mass_point]
        else:
            n = eejj_n["LQ"][i_mass_point]
            e = eejj_e["LQ"][i_mass_point]
            entries = eejj_entries ["LQ"][i_mass_point]

        if n!= 0.0:
            ln_f = 1.0 + e / n 
            weight = n / entries 
        else: 
            if background_name == "vv":
                ln_f = "blah"
                weight = 0.111
            elif background_name == "stop":
                ln_f = "blah"
                weight = 0.438
            elif background_name == "wjet":
                ln_f = "blah"
                weight = "1.20"
            elif background_name == "ttbar":
                ln_f = "blah"
                weight = "0.19"
            else:
                ln_f = "blah"
                weight = "blah"
        line_ln = "stat_Signal lnN " + str(ln_f)
        line_gm = "stat_Signal gmN " + str(int(entries)) + " " + str(ln_f)
        for i_background_name ,background_name in enumerate(background_names):
            line_ln = line_ln + " -"
            line_gm = line_gm + " -"
        
        card_file.write (line_ln + "\n")

        card_file.write("\n\n\n")
