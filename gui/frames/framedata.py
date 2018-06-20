from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
import os
from ..consts import *
from ..models import table_models
import pandas as pd
from engine.data import CSVDataFeed
import traceback
from datetime import datetime
from datetime import timedelta

class FrameData(QtWidgets.QWidget):
    def __init__(self,parent=None):
        super(FrameData,self).__init__(parent=parent)

        hlayout = QHBoxLayout(self)
        self.setLayout(hlayout)

        grid = QtWidgets.QGridLayout(self)
        hlayout.addLayout(grid,stretch=0)
        hlayout.addStretch(0)

        btn_loaddata = QPushButton('加载交易数据')
        btn_loaddata.clicked.connect(self.loaddata)
        grid.addWidget(btn_loaddata,0,1)

        self.status = QLabel('')
        grid.addWidget(self.status,0,2)

        grid.addWidget(QLabel('起始时间：'),1,0)
        dt_start =QDateEdit()
        dt_start.setCalendarPopup(True)
        grid.addWidget(dt_start,1,1)
        dt_start.setDate(datetime.now() - timedelta(days=365))
        self.dt_start = dt_start

        grid.addWidget(QLabel('结束时间：'),1,2)
        dt_end = QDateEdit()
        dt_end.setCalendarPopup(True)
        grid.addWidget(dt_end, 1, 3)
        dt_end.setDate(datetime.now())
        self.dt_end = dt_end


        grid.addWidget(QLabel('请选择策略：'),2,0)
        combo = QComboBox()
        combo.addItems(['买入并持有','随机买卖','海龟交易原则','深度强化学习'])
        grid.addWidget(combo,2,1)

        grid.addWidget(QPushButton('开始回测'),3,1)

    def loaddata(self):
        try:
            filename, filetype = QtWidgets.QFileDialog.getOpenFileName(self,
                                                                       "选取数据文件",
                                                                       os.getcwd() + '//data',
                                                                       "CSV Files (*.csv);;All Files (*)")  # 设置文件扩展名过滤,注意用双分号间隔
            # self.text_file.setText(filename)
            datafeed = CSVDataFeed(csv=filename)
            self.status.setText('加载数据：'+ str(len(datafeed.data)))
            start,end = datafeed.get_date_range()
            self.dt_start.setDate(datetime.strptime(start,'%Y-%m-%d'))
            self.dt_end.setDate(datetime.strptime(end, '%Y-%m-%d'))

            table = mgr_frames.get_frame(FRAMES.FRAME_DATA_TABLE)

            table.setModel(table_models.DataFrameTableModel(df=datafeed.data))
        except:
            print(traceback.print_exc())



