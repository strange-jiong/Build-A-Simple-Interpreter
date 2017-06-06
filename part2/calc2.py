#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-06-02 12:14:46
# @Link    : ${link}
# @Version : $Id$

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


# Token的类型
# EOF用来表明对词法分析来说已经没有输入词了
INTEGER, PLUS, MINUS, EOF = 'INTEGER', 'PLUS', 'MINUS', 'EOF'


class Token(object):

    def __init__(self, type, value):
        # token type: INTEGER, PLUS, MINUS, or EOF
        self.type = type
        # token value: non-negative integer value, '+', '-', or None
        self.value = value

    def __str__(self):
        """类实例的string表达

        Examples:
            Token(INTEGER, 3)
            Token(PLUS '+')
        """
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()


class Interpreter(object):

    def __init__(self, text):
        # client string input, e.g. "3 + 5", "12 - 5", etc
        self.text = text
        # self.pos 是 self.text的下标
        self.pos = 0
        # current token instance
        self.current_token = None
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception('Error parsing input')

    def advance(self):

        """增加pos指针值，使他指向当前变量"""
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None  # Indicates end of input
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        """从输入中返回一个多数字的整数"""
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def get_next_token(self):
        """语法分析器

        将输入变为一个个的tokens

        返回下一个token
        """
        while self.current_char is not None:

            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return Token(INTEGER, self.integer())

            if self.current_char == '+':
                self.advance()
                return Token(PLUS, '+')

            if self.current_char == '-':
                self.advance()
                return Token(MINUS, '-')

            self.error()

        return Token(EOF, None)

    def eat(self, token_type):

    	# 将当前token的type与传递进来的type进行比较，如果相同就“吃掉”当前token，将下一个token赋值给当前token，否则报错

        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()

    def expr(self):

        """解析Parser / Interpreter解释

        expr -> INTEGER PLUS INTEGER
        expr -> INTEGER MINUS INTEGER
        """
        # set current token to the first token taken from the input
        self.current_token = self.get_next_token()

        # 第一个 token 应该是一个 integer
        left = self.current_token
        self.eat(INTEGER)

        # 这里 当前token type应该是  '+' or '-'
        op = self.current_token
        if op.type == PLUS:
            self.eat(PLUS)
        else:
            self.eat(MINUS)

        #接下来的 token type应该是一个 integer
        right = self.current_token
        self.eat(INTEGER)
        # 当前token 被设置为EOF token

		# 输入的序列被扫描完毕，给出执行结果

        if op.type == PLUS:
            result = left.value + right.value
        else:
            result = left.value - right.value
        return result


def main():
    while True:
        try:
            # To run under Python3 replace 'raw_input' call
            # with 'input'
            text = raw_input('calc> ')
        except EOFError:
            break
        if not text:
            continue
        interpreter = Interpreter(text)
        result = interpreter.expr()
        print(result)

if __name__ == '__main__':
    main()
