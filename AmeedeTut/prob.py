import random
from manim import *
import numpy as np

def randomize_numbers(numbers):
    for num in numbers:
        value = random.uniform(0, 1)
        num.set_value(value)
        if value > 0.1:
            num.set_color(GREEN)
        else:
            num.set_color(RED)
            
def get_results(numbers):
    results = VGroup()
    for num in numbers:
        if num.get_value() > 0.1:
            result = (
                SVGMobject('tick.svg')
                .set_color(GREEN_C)
                .set(width = 0.3)
            )
        else:
            result = (
                SVGMobject('cross.svg')
                .set_color(RED_C)
                .set(width = 0.3)
            )
        
        result.next_to(num, DOWN, buff = 0.2)
        results.add(result)
    return results

class RandomNumb(Scene):
    def construct(self):
        numbers = VGroup()
        
        for x in range(28):
            num = DecimalNumber()
            numbers.add(num)
            
        randomize_numbers(numbers)
        
        numbers.set(width = 0.38)
        numbers.arrange(RIGHT, buff = 0.1)
        numbers.to_edge(UR)
        
        for k in range(10):
            self.play(UpdateFromFunc(numbers, randomize_numbers))
            self.wait()
            result = get_results(numbers)
            self.play(Write(result))
            self.wait()
            box = SurroundingRectangle(result)
            self.play(Create(box))
            self.play(FadeOut(box), FadeOut(result))
            
        self.wait()
        
        
        
        
def get_data_1(self):
    w = 0.2
    t_row1 = (
        VGroup(
            *[
                SVGMobject('tick.svg').set(width = w).set_color(GREEN)
                for i in range(10)
            ]
        )
        .arrange(RIGHT, buff = 0.2)
        .to_edge(UL, buff = 0.25)
    )
    t_row2 = (
        VGroup(
            *[
                SVGMobject('tick.svg').set(width = w).set_color(GREEN)
                for i in range(10)
            ]
        )
        .arrange(RIGHT, buff = 0.2)
        .next_to(t_row1, DOWN, buff = 0.25)
    )
    c_row1 = (
        VGroup(
            *[
                SVGMobject('cross.svg').set(width = w).set_color(RED)
                for i in range(10)
            ]
        )
        .arrange(RIGHT, buff = 0.2)
        .next_to(t_row2, DOWN, buff = 0.25)
    )
    c_row2 = (
        VGroup(
            *[
                SVGMobject('cross.svg').set(width = w).set_color(RED)
                for i in range(10)
            ]
        )
        .arrange(RIGHT, buff = 0.2)
        .next_to(c_row1, DOWN, buff = 0.25)
    )
    c_row3 = (
        VGroup(
            *[
                SVGMobject('cross.svg').set(width = w).set_color(RED)
                for i in range(10)
            ]
        )
        .arrange(RIGHT, buff = 0.2)
        .next_to(c_row2, DOWN, buff = 0.25)
    )
    result = VGroup(*t_row1, *t_row2, *c_row1, *c_row2, *c_row3)
    return result

class CLT(Scene):
    def construct(self):
        random.seed(123)
        data = get_data_1(self)
        axes = (
            Axes(
                x_range = [0, 1.2, 0.1],
                y_range = [0, 2.5],
                x_length = 10,
                y_length = 4
            )
            .to_edge(DL)
            .shift(UP * 0.2)
        )
        
        labels = axes.get_axis_labels(x_label = "\\hat{p}", y_label ='')
        
        x_axis_nums = VGroup()
        for i in range(11):
            num = (
                MathTex("\\frac{%3d}{10}" % i)
                .scale(0.6)
                .next_to(axes.x_axis.n2p(i/10 + 0.05), DOWN, buff = 0.1)
            )
            x_axis_nums.add(num)
            
        sample_counter = (
            Tex('Total samples: ')
            .scale(0.6)
            .to_edge(UR)
            .shift(LEFT * 0.6)
        )
        total_counter = (
            Tex('Sum of averages: ')
            .scale(0.6)
            .next_to(sample_counter, DOWN, aligned_edge = LEFT, buff = 0.4)
        )
        average_counter = (
            Tex("Average: $\\hat{p}$")
            .scale(0.6)
            .next_to(total_counter, DOWN, aligned_edge = LEFT, buff = 0.4)
        )
        tex = VGroup(sample_counter, total_counter, average_counter)
        
        self.play(
            LaggedStart(
                Create(data),
                Write(tex),
                Create(axes),
                Write(labels),
                Write(x_axis_nums),
                run_time = 4, 
                lag_ratio = 1
            )
        )
        self.wait()
        
        sample_count = 10
        poss_outcome = sample_count + 1
        
        counter_num = 0
        counter_number = (
            Integer(counter_num).scale(0.5)
            .next_to(sample_counter, RIGHT, buff = 0.2)
        )
        counter_number.add_updater(lambda m: m.set_value(counter_num))
        
        total_sum = 0
        total_number = (
            DecimalNumber(total_sum).scale(0.5)
            .next_to(total_counter, RIGHT, buff = 0.2)
        )
        total_number.add_updater(lambda m: m.set_value(total_sum))
        
        average = 0
        average_number = (
            DecimalNumber(average).scale(0.5)
            .next_to(average_counter, RIGHT, buff = 0.2)
        )
        average_number.add_updater(lambda m: m.set_value(average))
        
        self.add(counter_number, total_number, average_number)
        
        sums = [0] * poss_outcome
        
        for s in range(100):
            a = random.sample(range(0, 50), k = sample_count)
            
            sample_results = VGroup()
            boxes = VGroup()
            correct = 0
            for i in a:
                res = data[i]
                box = SurroundingRectangle(res)
                sample_results.add(res)
                boxes.add(box)
                if i < 20:
                    correct = correct + 1
                
            moved_result = sample_results.copy()
            
            self.play(Create(boxes))
            self.play(
                moved_result.animate.arrange(RIGHT * 0.3, buff = 0.3).to_edge(UP),
                FadeOut(boxes)
            )
            
            prop = DecimalNumber(num_decimal_places = 1)
            prop.set_value(correct / sample_count)
            prop.next_to(moved_result, RIGHT, buff = 0.3)
            
            axes_box = SurroundingRectangle(
                moved_result,
                stroke_color = WHITE,
                stroke_width = 0.2,
                fill_color = BLUE,
                fill_opacity = 0.8,
                buff = 0.1
            )
            stack_in_axes = VGroup(axes_box, moved_result)
            
            self.play(DrawBorderThenFill(axes_box))
            self.play(Write(prop))
            
            counter_num += 1
            total_sum += correct / sample_count
            average = total_sum / counter_num
            
            self.play(
                stack_in_axes.animate.next_to(x_axis_nums[correct], UP, buff = 0)
                .set(width = 0.77)
                .shift(UP * sums[correct]),
                FadeOut(prop)
            )
            
            sums[correct] += stack_in_axes.get_height()
            
        self.wait()
        
        sigma = np.sqrt(0.4 * 0.6 / 50)
        mu = 0.45
        
        def gauss(x, mu, sigma):
            return np.exp(-0.5 * ((x - mu) / sigma)**2) / (sigma * np.sqrt(2 * np.pi))
        
        h = sums[4] * 2.5 / 4
        graph = axes.plot(lambda x: gauss(x, mu, sigma) * h / 5.5 ,
                          x_range = [0, 1])
        self.play(Create(graph))
        self.wait()
               
        
            
        