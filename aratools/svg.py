from aratools.ponskaart import PonsKaart, CheckPoint, Etappe
import drawSvg as draw

def etappe_to_svg(etappe: Etappe) -> draw.Drawing:
    # a3 is 210 x 148 mm
    drawing = draw.Drawing(width=210, height=148)
    if len(etappe) % 2 == 0:
        n_upper = int(len(etappe) / 2)
        n_lower = n_upper
    else:
        n_upper = int(len(etappe) / 2) + 1
        n_lower = int(len(etappe) / 2)
    
