<?xml version='1.0' encoding='UTF-8'?>
<Project Type="Project" LVVersion="26008000">
	<Property Name="NI.LV.All.SaveVersion" Type="Str">26.0</Property>
	<Property Name="NI.LV.All.SourceOnly" Type="Bool">true</Property>
	<Item Name="My Computer" Type="My Computer">
		<Property Name="server.app.propertiesEnabled" Type="Bool">true</Property>
		<Property Name="server.control.propertiesEnabled" Type="Bool">true</Property>
		<Property Name="server.tcp.enabled" Type="Bool">false</Property>
		<Property Name="server.tcp.port" Type="Int">0</Property>
		<Property Name="server.tcp.serviceName" Type="Str">My Computer/VI Server</Property>
		<Property Name="server.tcp.serviceName.default" Type="Str">My Computer/VI Server</Property>
		<Property Name="server.vi.callsEnabled" Type="Bool">true</Property>
		<Property Name="server.vi.propertiesEnabled" Type="Bool">true</Property>
		<Property Name="specify.custom.address" Type="Bool">false</Property>
		<Item Name="ConfigAndFilters.vi" Type="VI" URL="../ConfigAndFilters.vi"/>
		<Item Name="Custom REST GET.vi" Type="VI" URL="../Custom REST GET.vi"/>
		<Item Name="DashboardHeader.ctl" Type="VI" URL="../DashboardHeader.ctl"/>
		<Item Name="DashboardHeader.vi" Type="VI" URL="../DashboardHeader.vi"/>
		<Item Name="MainDashboard.vi" Type="VI" URL="../MainDashboard.vi"/>
		<Item Name="MeasurementCluster.ctl" Type="VI" URL="../MeasurementCluster.ctl"/>
		<Item Name="SensorCluster.ctl" Type="VI" URL="../SensorCluster.ctl"/>
		<Item Name="TimestampMsToString.vi" Type="VI" URL="../TimestampMsToString.vi"/>
		<Item Name="Dependencies" Type="Dependencies"/>
		<Item Name="Build Specifications" Type="Build"/>
	</Item>
</Project>
