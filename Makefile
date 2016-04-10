retrainClassifier:
	cd flask/app; python -c "import transpose; transpose.transpose_all_songs_all_modes();"
	cd classifier; python -c "import find_mode; find_mode.make_classifier();"
	cd classifier; bash remove_.sh



