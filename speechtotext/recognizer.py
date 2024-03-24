from transformers import WhisperForConditionalGeneration, WhisperProcessor, WhisperConfig
from datasets import load_dataset, DatasetDict, Dataset, Audio

class Recognizer:
    def __init__(self, language="Japanese", task="transcribe") -> None:
        self.processor = WhisperProcessor.from_pretrained("openai/whisper-large-v3", language=language, task=task)
        self.trained_model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-large-v3").to('cuda')
        self.trained_model.config_max_target_positions = 1024
        self.trained_model.config.force_decoder_ids = self.processor.get_decoder_prompt_ids(language="ja", task=task)
        self.trained_model.config.suppress_tokens = []

    def get_text_from_wav(self, audio: Audio) -> str:
        common_voice = DatasetDict()
        common_voice["train"] = Dataset.from_dict({"audio": [audio]}).cast_column("audio", Audio(sampling_rate=16000))

        for i in range(len(common_voice["train"])):
            inputs = self.processor(common_voice["train"][i]["audio"]["array"], return_tensors="pt", sampling_rate=16000).to('cuda')
            input_features = inputs.input_features

            try:
                generated_ids = self.trained_model.generate(input_features=input_features, max_new_tokens=440)
                transcription = self.processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
                return transcription
            except Exception as e:
                print(e)
                continue