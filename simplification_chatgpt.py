import argparse
from tqdm import tqdm

from search_kNN import use_simcse

# import openai

# openai.api_key=''

def simplification_chatgpt(input_file, output_file):
    with open(input_file, 'r') as f:
        input_list = f.read().split('\n')

    with open(output_file, 'w') as f:
        for content in tqdm(input_list):
            if content != '':
                # kNN_sentences = use_simcse(content)
                # print(kNN_sentences)

                # prompt_asahi = f'I want you to replace my complex sentence with simple sentence(s). Keep the meaning same, but make them simpler. Output should be in Japanese, with spaces between morphemes.\nComplex:{comp_sent[0]}\nSimple:{simp_sent[0]}\nComplex:{comp_sent[1]}\nSimple:{simp_sent[1]}\nComplex:{comp_sent[2]}\nSimple:{simp_sent[2]}\nComplex:'+str(content)+'\nSimple: '
                # prompt_ehime = f'I want you to replace my complex sentence with simple sentence(s) by using the following as references. Keep the meaning the same, but make them simpler for higher elementary school students. Output should be in Japanese.\nComplex:{comp_sent[0]}\nSimple:{simp_sent[0]}\nComplex:{comp_sent[1]}\nSimple:{simp_sent[1]}\nComplex:{comp_sent[2]}\nSimple:{simp_sent[2]}\nComplex:'+str(content)+'\nSimple: '
                # response = openai.ChatCompletion.create(
                #     model='gpt-4',
                #     messages=[
                #         {'role': 'user', 'content': prompt}
                #     ]
                # )
                # f.write('%s\n' % response['choices'][0]['message']['content'])

    print('正常に終了しました。')


if __name__ =='__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--input_file', default='')
    parser.add_argument('--output_file', default='')
    args = parser.parse_args()

    simplification_chatgpt(args.input_file, args.output_file)