% reads in DOA excel files and computes the optimal threshold per patient
HOPPATS = {'PY04N007', 'PY04N008', 'PY04N012', 'PY04N013', 'PY04N015', ...
    'PY05N004', 'PY05N005', 'PY11N003', 'PY11N004', 'PY11N006', ...
    'PY12N005', 'PY12N008', 'PY12N010', 'PY12N012', 'PY13N001', ...
    'PY13N003', 'PY13N004', 'PY13N011', 'PY14N004', 'PY14N005'};



homeDir = '/Users/adam2392/Dropbox/EZTrack/Hopkins patients data/results/';
workDir = '/home/WIN/ali39/Dropbox/EZTrack/Hopkins patients data/results/';
if ~isempty(dir(homeDir)), rootDir = homeDir;
elseif ~isempty(dir(workDir)), rootDir = workDir;
else   error('Neither Work nor Home EEG directories exist! Exiting'); end

resultsFile = fullfile(rootDir, 'iEEG_all_CV_results_22-Jun-2015.mat');
data = load(resultsFile);

patients = fieldnames(data);
for iPat=1:length(patients)
    patient = patients{iPat};
    patData = data.(patient);
    
    % get the weights and the labels
    e_weights = patData.E_Weights;
    outcome = patData.Outcome;
    
    % ALL
    elec_labels = patData.E_labels;
    
    % CEZ
    resect_labels = patData.R_E_labels(~cellfun('isempty', patData.R_E_labels));
    
    % based on a certain threshold, compute EEZ for this dataset
    thresholds = linspace(0.1, 0.95, 100); % create range of thresholds to test
    
    % for each threshold, compute doa using jaccard index
    for iThresh=1:length(thresholds)
        threshold = thresholds(iThresh);
        
        % compute EEZ
        
        % compute Jaccard Index
        
    end
    
    % compute optimal threshold

end