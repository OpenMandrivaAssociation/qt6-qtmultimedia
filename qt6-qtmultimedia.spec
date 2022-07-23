%define beta beta2

Name:		qt6-qtmultimedia
Version:	6.4.0
Release:	%{?beta:0.%{beta}.}%{?snapshot:0.%{snapshot}.}1
%if 0%{?snapshot:1}
# "git archive"-d from "dev" branch of git://code.qt.io/qt/qtbase.git
Source:		qtmultimedia-%{?snapshot:%{snapshot}}%{!?snapshot:%{version}}.tar.zst
%else
Source:		http://download.qt-project.org/%{?beta:development}%{!?beta:official}_releases/qt/%(echo %{version}|cut -d. -f1-2)/%{version}%{?beta:-%{beta}}/submodules/qtmultimedia-everywhere-src-%{version}%{?beta:-%{beta}}.tar.xz
%endif
Patch0:		qtmultimedia-6.4.0-beta2-c++20.patch
Group:		System/Libraries
Summary:	Qt %{qtmajor} multimedia module
BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	cmake(Qt6Core)
BuildRequires:	cmake(Qt6Concurrent)
BuildRequires:	cmake(Qt6Gui)
BuildRequires:	cmake(Qt6Network)
BuildRequires:	cmake(Qt6Xml)
BuildRequires:	cmake(Qt6Widgets)
BuildRequires:	cmake(Qt6Sql)
BuildRequires:	cmake(Qt6Svg)
BuildRequires:	cmake(Qt6Test)
BuildRequires:	cmake(Qt6PrintSupport)
BuildRequires:	cmake(Qt6OpenGL)
BuildRequires:	cmake(Qt6OpenGLWidgets)
BuildRequires:	cmake(Qt6DBus)
BuildRequires:	cmake(Qt6Qml)
BuildRequires:	cmake(Qt6QmlModels)
BuildRequires:	cmake(Qt6QmlTools)
BuildRequires:	cmake(Qt6Quick)
BuildRequires:	cmake(Qt6QuickControls2)
BuildRequires:	cmake(Qt6QuickTemplates2)
BuildRequires:	cmake(Qt6QuickTest)
BuildRequires:	cmake(Qt6Quick3D)
BuildRequires:	cmake(Qt6Quick3DHelpers)
BuildRequires:	cmake(Qt6Quick3DTools)
BuildRequires:	cmake(Qt6Quick3DUtils)
BuildRequires:	cmake(Qt6AssimpImporterPlugin)
BuildRequires:	cmake(Qt6Quick3DAssetImport)
BuildRequires:	cmake(Qt6Quick3DAssetUtils)
BuildRequires:	cmake(Qt6BundledEmbree)
BuildRequires:	cmake(Qt6Quick3DEffects)
BuildRequires:	cmake(Qt6Quick3DGlslParserPrivate)
BuildRequires:	cmake(Qt6Quick3DIblBaker)
BuildRequires:	cmake(Qt6Quick3DParticleEffects)
BuildRequires:	cmake(Qt6Quick3DParticles)
BuildRequires:	cmake(Qt6Quick3DRuntimeRender)
BuildRequires:	cmake(Qt6ShaderTools)
BuildRequires:	qt6-qtdeclarative
BuildRequires:	qt6-qtquick3d
BuildRequires:	qt6-cmake
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(xkbcommon)
BuildRequires:	pkgconfig(vulkan)
BuildRequires:	pkgconfig(libva)
BuildRequires:	pkgconfig(libpulse)
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(libavcodec)
BuildRequires:	pkgconfig(gstreamer-1.0)
BuildRequires:	pkgconfig(gstreamer-base-1.0)
BuildRequires:	pkgconfig(gstreamer-audio-1.0)
BuildRequires:	pkgconfig(gstreamer-video-1.0)
BuildRequires:	pkgconfig(gstreamer-photography-1.0)
BuildRequires:	pkgconfig(gstreamer-pbutils-1.0)
BuildRequires:	cmake(LLVM)
BuildRequires:	cmake(Clang)
# Not really required, but referenced by LLVMExports.cmake
# (and then required because of the integrity check)
BuildRequires:	%{_lib}gpuruntime
License:	LGPLv3/GPLv3/GPLv2

%description
Qt %{qtmajor} multimedia module

%define extra_devel_files_Multimedia \
%{_qtdir}/lib/cmake/Qt6/FindAVFoundation.cmake \
%{_qtdir}/lib/cmake/Qt6/FindGObject.cmake \
%{_qtdir}/lib/cmake/Qt6/FindGStreamer.cmake \
%{_qtdir}/lib/cmake/Qt6/FindMMRenderer.cmake \
%{_qtdir}/lib/cmake/Qt6/FindWMF.cmake \
%{_qtdir}/lib/cmake/Qt6/FindWrapPulseAudio.cmake \
%{_qtdir}/lib/cmake/Qt6/FindFFmpeg.cmake \
%{_qtdir}/lib/cmake/Qt6/FindMMRendererCore.cmake \
%{_qtdir}/lib/cmake/Qt6/FindVAAPI.cmake \
%{_qtdir}/lib/cmake/Qt6/FindWrapBundledResonanceAudioConfigExtra.cmake \
%{_qtdir}/lib/cmake/Qt6BundledResonanceAudio \
%{_qtdir}/lib/libQt6BundledResonanceAudio.a

%define extra_files_Multimedia \
%dir %{_qtdir}/plugins/multimedia \
%{_qtdir}/plugins/multimedia/libffmpegmediaplugin.so \
%{_qtdir}/lib/cmake/Qt6Qml/QmlPlugins/*quickmultimedia*.cmake \
%{_qtdir}/qml/QtMultimedia

%global extra_files_Quick3DSpatialAudio \
%{_qtdir}/qml/QtQuick3D/SpatialAudio

%global extra_devel_files_Quick3DSpatialAudio \
%{_qtdir}/lib/cmake/Qt6Qml/QmlPlugins/*3dspatialaudio*

%qt6libs Multimedia MultimediaWidgets SpatialAudio MultimediaQuick Quick3DSpatialAudio

%package examples
Summary:	Example code demonstrating the use of %{name}
Group:		Development/KDE and Qt

%description examples
Example code demonstrating the use of %{name}

%files examples
%{_libdir}/qt6/examples/multimedia
%{_libdir}/qt6/examples/multimediawidgets

# No need to pull in dependency bloat, the ffmpeg plugin
# should be better anyway...
%package gstreamer
Summary:	Gstreamer based plugin for Qt multimedia playback
Group:		System/Libraries

%description gstreamer
Gstreamer based plugin for Qt multimedia playback

%files gstreamer
%{_qtdir}/plugins/multimedia/libgstreamermediaplugin.so

%prep
%autosetup -p1 -n qtmultimedia%{!?snapshot:-everywhere-src-%{version}%{?beta:-%{beta}}}
%cmake -G Ninja \
	-DCMAKE_INSTALL_PREFIX=%{_qtdir} \
	-DQT_BUILD_EXAMPLES:BOOL=ON \
	-DQT_WILL_INSTALL:BOOL=ON \
	-DFEATURE_spatialaudio_quick3d:BOOL=ON \
	--log-level=STATUS \
|| cat CMakeFiles/CMakeOutput.log

%build
export LD_LIBRARY_PATH="$(pwd)/build/lib:${LD_LIBRARY_PATH}"
%ninja_build -C build

%install
%ninja_install -C build
