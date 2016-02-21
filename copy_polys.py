import c4d
from c4d import utils

def main():
	class polys:
		def __init__ (self,ind,polygon):
			self.Id = ind
			self.polyst = polygon
			self.triangle = self.polyst.IsTriangle()
	obj = doc.GetActiveObject()
	all_polys = obj.GetAllPolygons()
	select = obj.GetPolygonS().GetAll(obj.GetPolygonCount())
	select_list = []
	for i in range(obj.GetPolygonCount()):### make select polys list
		a = polys(i,all_polys[i])
		if select[i] == 1 :
			select_list.append(a)
	for i in range(len(select_list)):### print select polys
		print select_list[i].Id ,"  ", select_list[i].polyst
	new_list = []
	for i in range(len(select_list)):
		polycount = obj.GetPolygonCount()
		pointcount = obj.GetPointCount()
		if select_list[i].triangle == 0 :
			n = []
			n.append(obj.GetPoint(select_list[i].polyst.a))
			n.append(obj.GetPoint(select_list[i].polyst.b))
			n.append(obj.GetPoint(select_list[i].polyst.c))
			n.append(obj.GetPoint(select_list[i].polyst.d))
			obj.ResizeObject(pointcount+4,polycount+1)
			index = []
			for k in range(len(n)):
				obj.SetPoint(pointcount+k,n[k])
				index.append(pointcount+k)
			poly = c4d.CPolygon(index[0],index[1],index[2],index[3])
			obj.SetPolygon(polycount,poly)
			obj.Message (c4d.MSG_UPDATE)

		else:
			n = []
			n.append(obj.GetPoint(select_list[i].polyst.a))
			n.append(obj.GetPoint(select_list[i].polyst.b))
			n.append(obj.GetPoint(select_list[i].polyst.c))
			obj.ResizeObject(pointcount+3,polycount+1)
			index = []
			for k in range(len(n)):
				obj.SetPoint(pointcount+k,n[k])
				index.append(pointcount+k)
			poly = c4d.CPolygon(index[0],index[1],index[2])
			obj.SetPolygon(polycount,poly)
			obj.Message (c4d.MSG_UPDATE)
		new_list.append(polycount)
	print new_list
	select = obj.GetPolygonS()
	select.DeselectAll()
	for i in range(len(new_list)):
		select.Select(new_list[i])
	settings = c4d.BaseContainer()
	settings[c4d.MDATA_OPTIMIZE_TOLERANCE] = 0.01
	settings[c4d.MDATA_OPTIMIZE_POINTS] = True
	settings[c4d.MDATA_OPTIMIZE_POLYGONS] = True
	settings[c4d.MDATA_OPTIMIZE_UNUSEDPOINTS] = True
	utils.SendModelingCommand(command = c4d.MCOMMAND_OPTIMIZE,
		list = [op],
		mode = c4d.MODELINGCOMMANDMODE_POLYGONSELECTION,
		bc = settings,
		doc = doc)

if __name__=='__main__':
	main()
c4d.EventAdd()