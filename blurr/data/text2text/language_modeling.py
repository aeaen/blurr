# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/01zb_data-text2text-language-modeling.ipynb (unless otherwise specified).

__all__ = ['HF_CausalLMBeforeBatchTransform']

# Cell
import torch, pdb
from transformers import *
from fastai.text.all import *

from ...utils import *
from ..core import *
from .core import *


logging.set_verbosity_error()

# Cell
class HF_CausalLMBeforeBatchTransform(HF_BeforeBatchTransform):
    def __init__(self, hf_arch, hf_tokenizer, max_length=None, padding=True, truncation=True,
                 is_split_into_words=False, n_tok_inps=1, ignore_token_id = CrossEntropyLossFlat().ignore_index,
                 tok_kwargs={}, **kwargs):

        super().__init__(hf_arch, hf_tokenizer, max_length=max_length, padding=padding, truncation=truncation,
                         is_split_into_words=is_split_into_words, n_tok_inps=n_tok_inps,
                         tok_kwargs=tok_kwargs.copy(), **kwargs)

        self.ignore_token_id = ignore_token_id

    def encodes(self, samples):
        # because no target is specific in CLM, fastai will duplicate the inputs (which is just the raw text)
        samples = super().encodes(samples)
        if (len(samples[0]) == 1): return samples

        updated_samples = []
        for s in samples:
            s[0]['labels'] = s[0]['input_ids'].clone()
            s[0]['labels'][s[0]['labels'] == self.hf_tokenizer.pad_token_id] = self.ignore_token_id
            targ_ids = s[0]['input_ids'].clone()

            updated_samples.append((s[0], targ_ids))

        return updated_samples